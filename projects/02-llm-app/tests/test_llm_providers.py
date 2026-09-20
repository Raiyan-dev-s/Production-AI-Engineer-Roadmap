import pytest

from app.llm.mock_provider import MockLLMProvider
from app.schemas.llm import ChatMessage


@pytest.mark.anyio
async def test_mock_provider_generate() -> None:
    provider = MockLLMProvider()
    messages = [ChatMessage(role="user", content="Hello")]
    response = await provider.generate(messages)

    assert len(response.content) > 0
    assert response.model == "mock-7b"
    assert response.usage.total_tokens > 0
    assert response.usage.prompt_tokens > 0
    assert response.usage.completion_tokens > 0


@pytest.mark.anyio
async def test_mock_provider_generate_with_model() -> None:
    provider = MockLLMProvider()
    messages = [ChatMessage(role="user", content="Hello")]
    response = await provider.generate(messages, model="mock-13b")

    assert response.model == "mock-13b"


@pytest.mark.anyio
async def test_mock_provider_generate_stream() -> None:
    provider = MockLLMProvider()
    messages = [ChatMessage(role="user", content="Hello")]
    chunks = []

    async for chunk in provider.generate_stream(messages):
        chunks.append(chunk)

    full_response = "".join(chunks)
    assert len(full_response) > 0


@pytest.mark.anyio
async def test_mock_provider_summarize_response() -> None:
    provider = MockLLMProvider()
    messages = [ChatMessage(role="user", content="Please summarize this text.")]
    response = await provider.generate(messages)

    assert len(response.content) > 0


@pytest.mark.anyio
async def test_mock_provider_classify_response() -> None:
    provider = MockLLMProvider()
    messages = [ChatMessage(role="user", content="Classify this as positive.")]
    response = await provider.generate(messages)

    assert len(response.content) > 0


@pytest.mark.anyio
async def test_mock_provider_get_model_info() -> None:
    provider = MockLLMProvider()
    info = await provider.get_model_info("mock-13b")

    assert info.id == "mock-13b"
    assert info.name == "Mock 13B"
    assert info.provider == "mock"


@pytest.mark.anyio
async def test_mock_provider_get_model_info_default() -> None:
    provider = MockLLMProvider()
    info = await provider.get_model_info()

    assert info.id == "mock-7b"


@pytest.mark.anyio
async def test_mock_provider_list_models() -> None:
    provider = MockLLMProvider()
    models = await provider.list_models()

    assert len(models) == 3
    model_ids = [m.id for m in models]
    assert "mock-7b" in model_ids
    assert "mock-13b" in model_ids
    assert "mock-70b" in model_ids
