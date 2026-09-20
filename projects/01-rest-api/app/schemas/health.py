"""Health check response schema."""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Schema for the health check endpoint."""

    status: str = Field("ok", examples=["ok"])
    version: str = Field("1.0.0", examples=["1.0.0"])
    database_status: str = Field("connected", examples=["connected", "disconnected"])
