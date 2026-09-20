"""Tests for the health check endpoint."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check_returns_ok(client: AsyncClient) -> None:
    """GET /api/health should return status 200 with 'ok' status."""
    response = await client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "1.0.0"
    assert data["database_status"] == "connected"


@pytest.mark.asyncio
async def test_health_check_has_required_fields(client: AsyncClient) -> None:
    """Health response must contain status, version, and database_status."""
    response = await client.get("/api/health")
    data = response.json()
    assert "status" in data
    assert "version" in data
    assert "database_status" in data
