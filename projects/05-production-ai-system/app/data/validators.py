from typing import Any

from app.core.config import settings
from app.core.exceptions import ValidationError


def validate_text_input(text: str, field_name: str = "input") -> str:
    """Validate and sanitize text input."""
    if not isinstance(text, str):
        raise ValidationError(f"{field_name} must be a string")

    text = text.strip()
    if not text:
        raise ValidationError(f"{field_name} cannot be empty")

    if len(text) > settings.MAX_INPUT_LENGTH:
        raise ValidationError(
            f"{field_name} exceeds maximum length of {settings.MAX_INPUT_LENGTH}",
            details={"length": len(text), "max": settings.MAX_INPUT_LENGTH},
        )

    return text


def validate_json_input(data: dict, required_fields: list[str]) -> dict:
    """Validate that a dict contains required fields."""
    if not isinstance(data, dict):
        raise ValidationError("Input must be a JSON object")

    missing = [f for f in required_fields if f not in data]
    if missing:
        raise ValidationError(
            f"Missing required fields: {', '.join(missing)}",
            details={"missing_fields": missing},
        )

    return data


def sanitize_output(text: str) -> str:
    """Sanitize model output before returning to the user.

    TODO: Add real sanitization:
    - Remove prompt injection markers
    - Strip PII (names, emails, phone numbers)
    - Remove sensitive system information
    - Validate encoding
    """
    if not isinstance(text, str):
        return text

    # Basic sanitization
    text = text.strip()
    # TODO: Add regex-based PII removal
    # TODO: Add prompt injection detection
    return text


def validate_batch_size(batch: list[Any]) -> list[Any]:
    """Validate batch size for batch inference."""
    if not isinstance(batch, list):
        raise ValidationError("Batch input must be a list")

    if len(batch) == 0:
        raise ValidationError("Batch cannot be empty")

    if len(batch) > settings.MAX_BATCH_SIZE:
        raise ValidationError(
            f"Batch size {len(batch)} exceeds maximum {settings.MAX_BATCH_SIZE}",
            details={"batch_size": len(batch), "max": settings.MAX_BATCH_SIZE},
        )

    return batch
