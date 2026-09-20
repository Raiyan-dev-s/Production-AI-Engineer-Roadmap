import logging
import sys

from app.core.config import settings


def setup_logging(name: str | None = None) -> logging.Logger:
    """Configure structured logging for the application.

    TODO: Add structured JSON logging for production:
    - Use python-json-logger for JSON format
    - Add correlation IDs (request_id)
    - Add model name, latency to log entries
    - Integrate with log aggregation (ELK, Datadog, CloudWatch)

    Example structured log:
        {"timestamp": "...", "level": "INFO", "logger": "app.ai.pipeline",
         "message": "Prediction complete", "model": "gpt-4",
         "latency_ms": 123.4, "request_id": "abc-123"}
    """
    logger = logging.getLogger(name or "app")

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)

    return logger
