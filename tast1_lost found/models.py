from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field


class StatusEnum(str, Enum):
    Lost = "Lost"
    Found = "Found"
    Returned = "Returned"


class ItemBase(SQLModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=3)
    category: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1)
    reported_by: str = Field(..., min_length=1)
    status: StatusEnum = StatusEnum.Lost


class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ItemCreate(ItemBase):
    """Schema used for POST /items"""
    pass


class ItemUpdate(SQLModel):
    """Schema used for PUT /items/{item_id} - all fields optional"""
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    reported_by: Optional[str] = None
    status: Optional[StatusEnum] = None


class ItemRead(ItemBase):
    """Schema used for responses"""
    id: int