from decimal import Decimal

from pydantic import BaseModel, Field
from uuid6 import uuid7


class MenuItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid7()), frozen=True)
    restaurant_id: str
    name: str = Field(min_length=1)
    price: float = Field(gt=0)
    description: str = ""
    available: bool = True

class MenuItemInput(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(gt=0)
    description: str = ""

class MenuItemOutput(BaseModel):
    id: str
    name: str
    price: float
    description: str

class MenuItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    price: float | None = Field(default=None, gt = 0)
    description: str | None = Field(default=None, min_length=1)
    available: bool | None = None
        