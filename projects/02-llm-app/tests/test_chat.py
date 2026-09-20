import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_health_check(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "provider" in data


@pytest.mark.anyio
async def test_chat_endpoint(client: AsyncClient) -> None:
    request_data = {
        "messages": [{"role": "user", "content": "Hello, how are you?"}],
    }
    response = await client.post("/api/chat", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "content" in data
    assert "model" in data
    assert "usage" in data
    assert len(data["content"]) > 0


@pytest.mark.anyio
async def test_chat_with_model_override(client: AsyncClient) -> None:
    request_data = {
        "messages": [{"role": "user", "content": "Tell me a joke"}],
        "model": "mock-13b",
    }
    response = await client.post("/api/chat", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data["model"] == "mock-13b"


@pytest.mark.anyio
async def test_chat_with_system_message(client: AsyncClient) -> None:
    request_data = {
        "messages": [
            {"role": "system", "content": "You are a pirate."},
            {"role": "user", "content": "Hello!"},
        ],
    }
    response = await client.post("/api/chat", json=request_data)
    assert response.status_code == 200
    assert len(response.json()["content"]) > 0


@pytest.mark.anyio
async def test_summarize_endpoint(client: AsyncClient) -> None:
    request_data = {
        "text": "Artificial intelligence is transforming industries worldwide. "
        "From healthcare to finance, AI systems are being deployed to improve "
        "efficiency and decision-making. However, concerns about bias, privacy, "
        "and job displacement remain significant challenges that need to be addressed.",
        "max_length": 50,
    }
    response = await client.post("/api/summarize", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "model" in data
    assert len(data["summary"]) > 0


@pytest.mark.anyio
async def test_classify_endpoint(client: AsyncClient) -> None:
    request_data = {
        "text": "This product is amazing! I love everything about it.",
        "categories": ["positive", "negative", "neutral"],
    }
    response = await client.post("/api/classify", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data["category"] in ["positive", "negative", "neutral"]
    assert 0.0 <= data["confidence"] <= 1.0


@pytest.mark.anyio
async def test_list_models(client: AsyncClient) -> None:
    response = await client.get("/api/models")
    assert response.status_code == 200
    models = response.json()
    assert isinstance(models, list)
    assert len(models) > 0
    for model in models:
        assert "id" in model
        assert "name" in model
        assert "provider" in model


@pytest.mark.anyio
async def test_chat_empty_messages(client: AsyncClient) -> None:
    response = await client.post("/api/chat", json={"messages": []})
    assert response.status_code == 422


@pytest.mark.anyio
async def test_classify_empty_categories(client: AsyncClient) -> None:
    request_data = {"text": "Some text", "categories": []}
    response = await client.post("/api/classify", json=request_data)
    assert response.status_code == 422
