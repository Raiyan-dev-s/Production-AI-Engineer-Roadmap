"""Tests for Item CRUD endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_item(client: AsyncClient) -> None:
    """POST /api/items should create and return a new item."""
    payload = {"name": "Test Item", "description": "A test description"}
    response = await client.post("/api/items", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "A test description"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_create_item_without_description(client: AsyncClient) -> None:
    """POST /api/items should allow a null description."""
    payload = {"name": "No Description"}
    response = await client.post("/api/items", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "No Description"
    assert data["description"] is None


@pytest.mark.asyncio
async def test_list_items(client: AsyncClient) -> None:
    """GET /api/items should return a list with total count."""
    await client.post("/api/items", json={"name": "Item 1"})
    await client.post("/api/items", json={"name": "Item 2"})
    response = await client.get("/api/items")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


@pytest.mark.asyncio
async def test_list_items_pagination(client: AsyncClient) -> None:
    """GET /api/items with skip and limit should paginate results."""
    for i in range(5):
        await client.post("/api/items", json={"name": f"Item {i}"})
    response = await client.get("/api/items?skip=2&limit=2")
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total"] == 5


@pytest.mark.asyncio
async def test_get_item(client: AsyncClient) -> None:
    """GET /api/items/{id} should return a single item."""
    create_resp = await client.post("/api/items", json={"name": "Fetch Me"})
    item_id = create_resp.json()["id"]
    response = await client.get(f"/api/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Fetch Me"


@pytest.mark.asyncio
async def test_get_item_not_found(client: AsyncClient) -> None:
    """GET /api/items/{id} with a bad ID should return 404."""
    response = await client.get("/api/items/nonexistent-id")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_item(client: AsyncClient) -> None:
    """PUT /api/items/{id} should update and return the modified item."""
    create_resp = await client.post("/api/items", json={"name": "Original"})
    item_id = create_resp.json()["id"]
    response = await client.put(f"/api/items/{item_id}", json={"name": "Updated"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated"


@pytest.mark.asyncio
async def test_delete_item(client: AsyncClient) -> None:
    """DELETE /api/items/{id} should remove the item."""
    create_resp = await client.post("/api/items", json={"name": "Delete Me"})
    item_id = create_resp.json()["id"]
    response = await client.delete(f"/api/items/{item_id}")
    assert response.status_code == 204
    get_resp = await client.get(f"/api/items/{item_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_item_not_found(client: AsyncClient) -> None:
    """DELETE /api/items/{id} with a bad ID should return 404."""
    response = await client.delete("/api/items/nonexistent-id")
    assert response.status_code == 404
