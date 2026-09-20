"""Item repository with item-specific queries."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item
from app.repositories.base import BaseRepository


class ItemRepository(BaseRepository[Item]):
    """CRUD operations specific to the Item model."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Item, session)
