from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from app.schemas.llm import ChatMessage, ChatResponse, ModelInfo


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    async def generate(
        self,
        messages: list[ChatMessage],
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> ChatResponse:
        """Generate a response from the LLM."""
        ...

    @abstractmethod
    async def generate_stream(
        self,
        messages: list[ChatMessage],
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> AsyncIterator[str]:
        """Generate a streamed response from the LLM."""
        ...
        yield  # make this a generator
        return  # pragma: no cover

    @abstractmethod
    async def get_model_info(self, model: str | None = None) -> ModelInfo:
        """Get information about the specified model."""
        ...

    @abstractmethod
    async def list_models(self) -> list[ModelInfo]:
        """List all available models."""
        ...
