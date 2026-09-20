class LLMServiceError(Exception):
    """Base exception for LLM service errors."""

    def __init__(
        self, message: str = "LLM service error", status_code: int = 500
    ) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class RateLimitError(LLMServiceError):
    """Raised when the LLM provider rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded") -> None:
        super().__init__(message=message, status_code=429)


class ModelNotFoundError(LLMServiceError):
    """Raised when the requested model is not available."""

    def __init__(self, model: str = "") -> None:
        message = f"Model not found: {model}" if model else "Model not found"
        super().__init__(message=message, status_code=404)


class ProviderNotInstalledError(LLMServiceError):
    """Raised when the required provider package is not installed."""

    def __init__(self, provider: str = "") -> None:
        message = (
            f"Provider '{provider}' package not installed. "
            f"Install it with: pip install {provider}"
        )
        super().__init__(message=message, status_code=500)


class ProviderNotConfiguredError(LLMServiceError):
    """Raised when the provider is not properly configured."""

    def __init__(self, provider: str = "") -> None:
        message = f"Provider '{provider}' is not configured. Check your environment variables."
        super().__init__(message=message, status_code=500)
