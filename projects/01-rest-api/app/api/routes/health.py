"""Health check route."""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.health import HealthResponse

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check(db: AsyncSession = Depends(get_db)) -> HealthResponse:
    """Return application health including database connectivity."""
    database_status = "connected"
    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        database_status = "disconnected"

    return HealthResponse(
        status="ok",
        version="1.0.0",
        database_status=database_status,
    )
