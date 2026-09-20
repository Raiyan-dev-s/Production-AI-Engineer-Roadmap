"""Item CRUD routes."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.repositories.item import ItemRepository
from app.schemas.item import ItemCreate, ItemList, ItemResponse, ItemUpdate
from app.services.item import ItemService

router = APIRouter(prefix="/api/items", tags=["items"])


def _get_service(db: AsyncSession = Depends(get_db)) -> ItemService:
    """Build and return an ItemService with its repository wired up."""
    repository = ItemRepository(db)
    return ItemService(repository)


@router.get("", response_model=ItemList)
async def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service: ItemService = Depends(_get_service),
) -> ItemList:
    """Return a paginated list of all items."""
    return await service.get_items(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: str,
    service: ItemService = Depends(_get_service),
) -> ItemResponse:
    """Return a single item by its ID."""
    return await service.get_item(item_id)


@router.post("", response_model=ItemResponse, status_code=201)
async def create_item(
    item_in: ItemCreate,
    service: ItemService = Depends(_get_service),
) -> ItemResponse:
    """Create a new item and return it."""
    return await service.create_item(item_in)


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: str,
    item_in: ItemUpdate,
    service: ItemService = Depends(_get_service),
) -> ItemResponse:
    """Update an existing item and return the result."""
    return await service.update_item(item_id, item_in)


@router.delete("/{item_id}", status_code=204)
async def delete_item(
    item_id: str,
    service: ItemService = Depends(_get_service),
) -> None:
    """Delete an item by its ID."""
    await service.delete_item(item_id)
