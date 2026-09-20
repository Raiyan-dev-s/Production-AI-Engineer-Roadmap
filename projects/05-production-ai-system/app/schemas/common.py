from typing import Any

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: dict[str, Any] | None = None


class ErrorResponse(BaseModel):
    error: ErrorDetail


class StandardResponse[T](BaseModel):
    """Standard API response wrapper."""

    success: bool = True
    data: T | None = None
    error: ErrorDetail | None = None
    request_id: str | None = None


class PaginatedResponse[T](BaseModel):
    """Paginated list response."""

    items: list[T]
    total: int
    page: int = 1
    page_size: int = 20
    has_next: bool = False


class PaginationParams(BaseModel):
    """Pagination query parameters."""

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str
    models_loaded: list[str] = []


class MetricsSummary(BaseModel):
    total_requests: int = 0
    total_errors: int = 0
    avg_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0
