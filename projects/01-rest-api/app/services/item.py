"""Item service containing business logic."""

from typing import Any

from app.core.exceptions import NotFoundException, ValidationException
from app.repositories.item import ItemRepository
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:
    """Orchestrates business logic for Items, delegating persistence to the repository."""

    def __init__(self, repository: ItemRepository) -> None:
        self.repository = repository

    async def get_item(self, item_id: str) -> Any:
        """Retrieve a single item by ID or raise NotFoundException."""
        item = await self.repository.get(item_id)
        if item is None:
            raise NotFoundException(f"Item with id '{item_id}' not found")
        return item

    async def get_items(self, skip: int = 0, limit: int = 100) -> Any:
        """Return a paginated list of items along with the total count."""
        items = await self.repository.get_all(skip=skip, limit=limit)
        total = await self.repository.count()
        return {"items": items, "total": total}

    async def create_item(self, item_in: ItemCreate) -> Any:
        """Create a new item after validating input."""
        if not item_in.name or not item_in.name.strip():
            raise ValidationException("Item name must not be empty")
        data = item_in.model_dump()
        return await self.repository.create(data)

    async def update_item(self, item_id: str, item_in: ItemUpdate) -> Any:
        """Update an existing item. Raises NotFoundException if missing."""
        item = await self.get_item(item_id)
        update_data = item_in.model_dump(exclude_unset=True)
        if not update_data:
            raise ValidationException("No fields to update")
        return await self.repository.update(item, update_data)

    async def delete_item(self, item_id: str) -> None:
        """Delete an item by ID. Raises NotFoundException if missing."""
        item = await self.get_item(item_id)
        await self.repository.delete(item)
