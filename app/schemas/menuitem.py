from pydantic import UUID7, BaseModel, Field
from uuid6 import uuid7
from decimal import Decimal

class MenuItem(BaseModel):
    id: UUID7 = Field(default_factory=uuid7, frozen=True)

    restaurant_id: UUID7 = Field(default_factory=uuid7, frozen=True)

    name: str = Field(min_length=1)

    description: str = Field(min_length=1)

    price: Decimal = Field(ge=0, decimal_places=2)

    active: bool = True