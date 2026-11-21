from decimal import Decimal
from pydantic import AliasChoices, BaseModel, Field, PositiveInt
from app.schemas.common import Price, CartQuantity


class CartItem(BaseModel):
    menu_item_id: str = Field(frozen=True)
    quantity: PositiveInt
    price: Price = Field(frozen=True, gt=Decimal("0.00"))

class Cart(BaseModel):
    customer_id: str = Field(
        validation_alias=AliasChoices("customer_id", "id"),
        serialization_alias="id",
        frozen=True,
    )
    restaurant_id: str = Field(frozen=True)
    items: list[CartItem] = Field(default_factory=list)
    subtotal: Price = Field(default=Decimal("0.00"))

class CartItemAdd(BaseModel):
    menu_item_id: str
    quantity: PositiveInt = Field(default=1)

class CartCreate(CartItemAdd):
    customer_id: str = Field(min_length =1)

class CartItemResponse(BaseModel):
    menu_item_name: str
    quantity: CartQuantity
    price: Price

class CartResponse(BaseModel):
    restaurant_name: str
    items: list[CartItemResponse] = Field(default_factory=list)
    total_quantity: int = Field(ge=0)
    sub_total: Price = Field(default=Decimal("0.00"))