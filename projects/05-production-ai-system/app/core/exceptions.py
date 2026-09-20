from typing import Any


class AppException(Exception):
    """Base application exception."""

    def __init__(
        self,
        message: str,
        error_code: str = "APP_ERROR",
        status_code: int = 500,
        details: dict[str, Any] | None = None,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class ValidationError(AppException):
    """Input validation failed."""

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=400,
            details=details,
        )


class ModelNotFoundError(AppException):
    """Requested model not found or not loaded."""

    def __init__(self, model_name: str):
        super().__init__(
            message=f"Model '{model_name}' not found",
            error_code="MODEL_NOT_FOUND",
            status_code=404,
            details={"model_name": model_name},
        )


class ModelLoadError(AppException):
    """Failed to load a model."""

    def __init__(self, model_name: str, reason: str = ""):
        super().__init__(
            message=f"Failed to load model '{model_name}': {reason}",
            error_code="MODEL_LOAD_ERROR",
            status_code=500,
            details={"model_name": model_name, "reason": reason},
        )


class InferenceError(AppException):
    """Model inference failed."""

    def __init__(self, model_name: str, reason: str = ""):
        super().__init__(
            message=f"Inference failed for model '{model_name}': {reason}",
            error_code="INFERENCE_ERROR",
            status_code=500,
            details={"model_name": model_name, "reason": reason},
        )


class RateLimitError(AppException):
    """Rate limit exceeded."""

    def __init__(self, retry_after: float = 60.0):
        super().__init__(
            message="Rate limit exceeded",
            error_code="RATE_LIMITED",
            status_code=429,
            details={"retry_after_seconds": retry_after},
        )
