from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

from app.llm.mock_provider import MockLLMProvider
from app.services.chat import ChatService


@pytest.fixture
def mock_provider() -> MockLLMProvider:
    return MockLLMProvider()


@pytest.fixture
def chat_service(mock_provider: MockLLMProvider) -> ChatService:
    return ChatService(provider=mock_provider)


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    from app.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
