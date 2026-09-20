import pytest

from app.llm.mock_provider import MockLLMProvider
from app.schemas.llm import (
    ChatMessage,
    ChatRequest,
    ClassifyRequest,
    SummarizeRequest,
)
from app.services.chat import ChatService


@pytest.mark.anyio
async def test_chat_service_chat() -> None:
    provider = MockLLMProvider()
    service = ChatService(provider=provider)
    request = ChatRequest(
        messages=[ChatMessage(role="user", content="Hello")],
    )
    response = await service.chat(request)

    assert len(response.content) > 0
    assert response.model.startswith("mock")


@pytest.mark.anyio
async def test_chat_service_chat_with_model() -> None:
    provider = MockLLMProvider()
    service = ChatService(provider=provider)
    request = ChatRequest(
        messages=[ChatMessage(role="user", content="Hello")],
        model="mock-70b",
    )
    response = await service.chat(request)

    assert response.model == "mock-70b"


@pytest.mark.anyio
async def test_chat_service_summarize() -> None:
    provider = MockLLMProvider()
    service = ChatService(provider=provider)
    request = SummarizeRequest(
        text="This is a long text that needs to be summarized for the user.",
        max_length=50,
    )
    response = await service.summarize(request)

    assert len(response.summary) > 0
    assert response.model.startswith("mock")
    assert response.usage.total_tokens > 0


@pytest.mark.anyio
async def test_chat_service_classify() -> None:
    provider = MockLLMProvider()
    service = ChatService(provider=provider)
    request = ClassifyRequest(
        text="This is great news!",
        categories=["positive", "negative", "neutral"],
    )
    response = await service.classify(request)

    assert response.category in ["positive", "negative", "neutral"]
    assert 0.0 <= response.confidence <= 1.0
    assert response.model.startswith("mock")


@pytest.mark.anyio
async def test_chat_service_classify_single_category() -> None:
    provider = MockLLMProvider()
    service = ChatService(provider=provider)
    request = ClassifyRequest(
        text="Some text to classify",
        categories=["spam", "not_spam"],
    )
    response = await service.classify(request)

    assert response.category in ["spam", "not_spam"]
    assert 0.0 <= response.confidence <= 1.0


@pytest.mark.anyio
async def test_chat_service_stream() -> None:
    provider = MockLLMProvider()
    service = ChatService(provider=provider)
    request = ChatRequest(
        messages=[ChatMessage(role="user", content="Hello")],
    )

    chunks = []
    async for chunk in service.chat_stream(request):
        chunks.append(chunk)

    assert len(chunks) > 0
    full_response = "".join(chunks)
    assert len(full_response) > 0


@pytest.mark.anyio
async def test_chat_service_prompt_templates_used() -> None:
    provider = MockLLMProvider()
    service = ChatService(provider=provider)

    request = SummarizeRequest(text="Some text to summarize")
    response = await service.summarize(request)
    assert len(response.summary) > 0

    request = ClassifyRequest(
        text="Some text",
        categories=["a", "b", "c"],
    )
    response = await service.classify(request)
    assert response.category in ["a", "b", "c"]
