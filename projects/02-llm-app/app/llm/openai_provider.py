from collections.abc import AsyncIterator

from app.core.config import settings
from app.core.exceptions import ProviderNotConfiguredError, ProviderNotInstalledError
from app.llm.base import LLMProvider
from app.schemas.llm import ChatMessage, ChatResponse, ModelInfo, TokenUsage

try:
    import openai

    OPENAI_INSTALLED = True
except ImportError:
    OPENAI_INSTALLED = False


OPENAI_MODELS = [
    ModelInfo(
        id="gpt-3.5-turbo", name="GPT-3.5 Turbo", provider="openai", max_tokens=4096
    ),
    ModelInfo(id="gpt-4", name="GPT-4", provider="openai", max_tokens=8192),
    ModelInfo(
        id="gpt-4-turbo", name="GPT-4 Turbo", provider="openai", max_tokens=128000
    ),
    ModelInfo(id="gpt-4o", name="GPT-4o", provider="openai", max_tokens=128000),
    ModelInfo(
        id="gpt-4o-mini", name="GPT-4o Mini", provider="openai", max_tokens=128000
    ),
]


class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider."""

    def __init__(self) -> None:
        if not OPENAI_INSTALLED:
            raise ProviderNotInstalledError("openai")

        if not settings.OPENAI_API_KEY:
            raise ProviderNotConfiguredError("openai")

        self._client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self._default_model = settings.MODEL_NAME or "gpt-3.5-turbo"

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

        response = await self._client.chat.completions.create(
            model=target_model,
            messages=[{"role": m.role, "content": m.content} for m in messages],
            max_tokens=max_tok,
            temperature=temp,
        )

        choice = response.choices[0]
        usage = response.usage

        return ChatResponse(
            content=choice.message.content or "",
            model=response.model,
            usage=TokenUsage(
                prompt_tokens=usage.prompt_tokens if usage else 0,
                completion_tokens=usage.completion_tokens if usage else 0,
                total_tokens=usage.total_tokens if usage else 0,
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

        stream = await self._client.chat.completions.create(
            model=target_model,
            messages=[{"role": m.role, "content": m.content} for m in messages],
            max_tokens=max_tok,
            temperature=temp,
            stream=True,
        )

        async for chunk in stream:
            delta = chunk.choices[0].delta if chunk.choices else None
            if delta and delta.content:
                yield delta.content

    async def get_model_info(self, model: str | None = None) -> ModelInfo:
        target_model = model or self._default_model
        for m in OPENAI_MODELS:
            if m.id == target_model:
                return m
        return ModelInfo(
            id=target_model, name=target_model, provider="openai", max_tokens=4096
        )

    async def list_models(self) -> list[ModelInfo]:
        return OPENAI_MODELS.copy()
