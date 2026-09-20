"""Item service containing business logic."""

from app.core.exceptions import NotFoundException, ValidationException
from app.repositories.item import ItemRepository
from app.schemas.item import ItemCreate, ItemList, ItemResponse, ItemUpdate


class ItemService:
    """Orchestrates business logic for Items, delegating persistence to the repository."""

    def __init__(self, repository: ItemRepository) -> None:
        self.repository = repository

    async def get_item(self, item_id: str) -> ItemResponse:
        """Retrieve a single item by ID or raise NotFoundException."""
        item = await self.repository.get(item_id)
        if item is None:
            raise NotFoundException(f"Item with id '{item_id}' not found")
        return ItemResponse.model_validate(item)

    async def get_items(self, skip: int = 0, limit: int = 100) -> ItemList:
        """Return a paginated list of items along with the total count."""
        items = await self.repository.get_all(skip=skip, limit=limit)
        total = await self.repository.count()
        return ItemList(
            items=[ItemResponse.model_validate(i) for i in items],
            total=total,
        )

    async def create_item(self, item_in: ItemCreate) -> ItemResponse:
        """Create a new item after validating input."""
        if not item_in.name or not item_in.name.strip():
            raise ValidationException("Item name must not be empty")
        data = item_in.model_dump()
        item = await self.repository.create(data)
        return ItemResponse.model_validate(item)

    async def update_item(self, item_id: str, item_in: ItemUpdate) -> ItemResponse:
        """Update an existing item. Raises NotFoundException if missing."""
        item = await self.repository.get(item_id)
        if item is None:
            raise NotFoundException(f"Item with id '{item_id}' not found")
        update_data = item_in.model_dump(exclude_unset=True)
        if not update_data:
            raise ValidationException("No fields to update")
        updated = await self.repository.update(item, update_data)
        return ItemResponse.model_validate(updated)

    async def delete_item(self, item_id: str) -> None:
        """Delete an item by ID. Raises NotFoundException if missing."""
        item = await self.repository.get(item_id)
        if item is None:
            raise NotFoundException(f"Item with id '{item_id}' not found")
        await self.repository.delete(item)
