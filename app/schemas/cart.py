from decimal import Decimal
from pydantic import BaseModel, Field, PositiveInt
from app.schemas.common import Price


class CartItem(BaseModel):
    menu_item_id: str = Field(frozen=True)
    quantity: PositiveInt
    price_per_item: Price = Field(alias="price", frozen=True, gt=Decimal("0.00"))

class Cart(BaseModel):
    customer_id: str = Field(serialization_alias="id", frozen=True)
    restaurant_id: str = Field(frozen=True)
    items: list[CartItem] = Field(default_factory=list)
    subtotal: Price = Field(default=Decimal("0.00"), frozen=True)

class CartItemAdd(BaseModel):
    menu_item_id: str
    quantity: PositiveInt = Field(default=1)

class CartCreate(CartItemAdd):
    customer_id: str = Field(min_length =1)

    
