"""Pydantic schemas for Item CRUD operations."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ItemCreate(BaseModel):
    """Schema for creating a new item."""

    name: str = Field(..., min_length=1, max_length=255, examples=["My Item"])
    description: str | None = Field(None, examples=["A description of the item"])


class ItemUpdate(BaseModel):
    """Schema for updating an existing item."""

    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None


class ItemResponse(BaseModel):
    """Schema for returning an item to the client."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime


class ItemList(BaseModel):
    """Schema for returning a list of items."""

    items: list[ItemResponse]
    total: int
