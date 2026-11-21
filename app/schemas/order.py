from datetime import datetime

from pydantic import BaseModel, Field, PlainSerializer, PositiveInt
from typing_extensions import Annotated, Literal
from uuid6 import uuid7

from app.schemas.common import Price

OrderStatus = Literal["pending", "confirmed", "preparing", "ready", "picked up", "delivered", "cancelled"]

OrderDate = Annotated[datetime, PlainSerializer(lambda x: x.isoformat(), return_type=str)]

class OrderItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid7()), frozen=True)
    order_id: str
    menu_item_id: str
    quantity: PositiveInt
    price_per_item: Price

class Order(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid7()), frozen=True)
    customer_id: str
    restaurant_id: str
    order_date: OrderDate = Field(default_factory=datetime.now)
    status: OrderStatus = "pending"
    total: Price

class OrderCreate(BaseModel):
    customer_id: str

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

class OrderItemResponse(BaseModel):
    menu_item_name: str
    quantity: PositiveInt
    price_per_item: Price

class OrderResponse(BaseModel):
    order_id: str
    customer_name: str
    restaurant_name: str
    order_date: OrderDate
    status: OrderStatus
    total: Price
    items: list[OrderItemResponse]