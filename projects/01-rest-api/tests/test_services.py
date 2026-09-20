"""Unit tests for ItemService with a mocked repository."""

from unittest.mock import AsyncMock

import pytest

from app.core.exceptions import NotFoundException, ValidationException
from app.schemas.item import ItemCreate, ItemUpdate
from app.services.item import ItemService


def _build_service() -> ItemService:
    """Return an ItemService backed by an AsyncMock repository."""
    mock_repo = AsyncMock()
    return ItemService(mock_repo), mock_repo


@pytest.mark.asyncio
async def test_get_item_found() -> None:
    """get_item should return the item when the repository finds it."""
    service, mock_repo = _build_service()
    fake_item = {"id": "1", "name": "Test"}
    mock_repo.get.return_value = fake_item
    result = await service.get_item("1")
    assert result == fake_item
    mock_repo.get.assert_awaited_once_with("1")


@pytest.mark.asyncio
async def test_get_item_not_found() -> None:
    """get_item should raise NotFoundException when the item does not exist."""
    service, mock_repo = _build_service()
    mock_repo.get.return_value = None
    with pytest.raises(NotFoundException):
        await service.get_item("missing")


@pytest.mark.asyncio
async def test_get_items() -> None:
    """get_items should return items and total from the repository."""
    service, mock_repo = _build_service()
    mock_repo.get_all.return_value = [{"id": "1"}]
    mock_repo.count.return_value = 1
    result = await service.get_items(skip=0, limit=10)
    assert result["items"] == [{"id": "1"}]
    assert result["total"] == 1


@pytest.mark.asyncio
async def test_create_item() -> None:
    """create_item should delegate to repository.create with extracted data."""
    service, mock_repo = _build_service()
    mock_repo.create.return_value = {"id": "1", "name": "New"}
    item_in = ItemCreate(name="New", description="desc")
    result = await service.create_item(item_in)
    mock_repo.create.assert_awaited_once_with({"name": "New", "description": "desc"})
    assert result["name"] == "New"


@pytest.mark.asyncio
async def test_create_item_empty_name() -> None:
    """create_item should reject an empty name with ValidationException."""
    service, _ = _build_service()
    item_in = ItemCreate(name="   ")
    with pytest.raises(ValidationException):
        await service.create_item(item_in)


@pytest.mark.asyncio
async def test_update_item() -> None:
    """update_item should merge partial data and call repository.update."""
    service, mock_repo = _build_service()
    existing = {"id": "1", "name": "Old", "description": "old desc"}
    mock_repo.get.return_value = existing
    mock_repo.update.return_value = {
        "id": "1",
        "name": "New",
        "description": "old desc",
    }
    item_in = ItemUpdate(name="New")
    result = await service.update_item("1", item_in)
    mock_repo.update.assert_awaited_once_with(existing, {"name": "New"})
    assert result["name"] == "New"


@pytest.mark.asyncio
async def test_update_item_empty_payload() -> None:
    """update_item should raise ValidationException when no fields are sent."""
    service, mock_repo = _build_service()
    mock_repo.get.return_value = {"id": "1", "name": "X"}
    item_in = ItemUpdate()
    with pytest.raises(ValidationException):
        await service.update_item("1", item_in)


@pytest.mark.asyncio
async def test_delete_item() -> None:
    """delete_item should call repository.delete after confirming the item exists."""
    service, mock_repo = _build_service()
    mock_repo.get.return_value = {"id": "1", "name": "X"}
    await service.delete_item("1")
    mock_repo.delete.assert_awaited_once_with({"id": "1", "name": "X"})
