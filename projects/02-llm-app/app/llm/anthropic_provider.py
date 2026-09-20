from collections.abc import AsyncIterator
from typing import Any

from app.core.config import settings
from app.core.exceptions import ProviderNotConfiguredError, ProviderNotInstalledError
from app.llm.base import LLMProvider
from app.schemas.llm import ChatMessage, ChatResponse, ModelInfo, TokenUsage

try:
    import anthropic

    ANTHROPIC_INSTALLED = True
except ImportError:
    ANTHROPIC_INSTALLED = False


ANTHROPIC_MODELS = [
    ModelInfo(
        id="claude-3-5-sonnet-20241022",
        name="Claude 3.5 Sonnet",
        provider="anthropic",
        max_tokens=200000,
    ),
    ModelInfo(
        id="claude-3-5-haiku-20241022",
        name="Claude 3.5 Haiku",
        provider="anthropic",
        max_tokens=200000,
    ),
    ModelInfo(
        id="claude-3-opus-20240229",
        name="Claude 3 Opus",
        provider="anthropic",
        max_tokens=200000,
    ),
]


class AnthropicProvider(LLMProvider):
    """Anthropic LLM provider."""

    def __init__(self) -> None:
        if not ANTHROPIC_INSTALLED:
            raise ProviderNotInstalledError("anthropic")

        if not settings.ANTHROPIC_API_KEY:
            raise ProviderNotConfiguredError("anthropic")

        self._client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        self._default_model = settings.MODEL_NAME or "claude-3-5-sonnet-20241022"

    async def generate(
        self,
        messages: list[ChatMessage],
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> ChatResponse:
        target_model = model or self._default_model
        max_tok = max_tokens or settings.MAX_TOKENS
        temp = temperature if temperature is not None else settings.TEMPERATURE

        system_message = ""
        chat_messages: list[dict[str, str]] = []
        for m in messages:
            if m.role == "system":
                system_message = m.content
            else:
                chat_messages.append({"role": m.role, "content": m.content})

        kwargs: dict[str, Any] = {
            "model": target_model,
            "messages": chat_messages,
            "max_tokens": max_tok,
            "temperature": temp,
        }
        if system_message:
            kwargs["system"] = system_message

        response = await self._client.messages.create(**kwargs)

        content = ""
        for block in response.content:
            if hasattr(block, "text"):
                content += block.text

        return ChatResponse(
            content=content,
            model=response.model,
            usage=TokenUsage(
                prompt_tokens=response.usage.input_tokens,
                completion_tokens=response.usage.output_tokens,
                total_tokens=response.usage.input_tokens + response.usage.output_tokens,
            ),
        )

    async def generate_stream(
        self,
        messages: list[ChatMessage],
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> AsyncIterator[str]:
        target_model = model or self._default_model
        max_tok = max_tokens or settings.MAX_TOKENS
        temp = temperature if temperature is not None else settings.TEMPERATURE

        system_message = ""
        chat_messages: list[dict[str, str]] = []
        for m in messages:
            if m.role == "system":
                system_message = m.content
            else:
                chat_messages.append({"role": m.role, "content": m.content})

        kwargs: dict[str, Any] = {
            "model": target_model,
            "messages": chat_messages,
            "max_tokens": max_tok,
            "temperature": temp,
        }
        if system_message:
            kwargs["system"] = system_message

        async with self._client.messages.stream(**kwargs) as stream:
            async for text in stream.text_stream:
                yield text

    async def get_model_info(self, model: str | None = None) -> ModelInfo:
        target_model = model or self._default_model
        for m in ANTHROPIC_MODELS:
            if m.id == target_model:
                return m
        return ModelInfo(
            id=target_model, name=target_model, provider="anthropic", max_tokens=200000
        )

    async def list_models(self) -> list[ModelInfo]:
        return ANTHROPIC_MODELS.copy()
