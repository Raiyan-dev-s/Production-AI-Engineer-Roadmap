from app.core.config import Settings
from app.core.exceptions import LLMServiceError
from app.llm.base import LLMProvider


def get_llm_provider(config: Settings | None = None) -> LLMProvider:
    """Factory function that returns the appropriate LLM provider based on config."""
    from app.core.config import settings as default_settings

    cfg = config or default_settings
    provider_name = cfg.LLM_PROVIDER.lower()

    if provider_name == "mock":
        from app.llm.mock_provider import MockLLMProvider

        return MockLLMProvider()

    if provider_name == "openai":
        from app.llm.openai_provider import OpenAIProvider

        return OpenAIProvider()

    if provider_name == "anthropic":
        from app.llm.anthropic_provider import AnthropicProvider

        return AnthropicProvider()

    raise LLMServiceError(
        message=f"Unknown LLM provider: '{provider_name}'. Supported: mock, openai, anthropic.",
        status_code=500,
    )
