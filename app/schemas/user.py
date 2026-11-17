from uuid6 import uuid7
from typing_extensions import Annotated, Literal, Union
from pydantic import BaseModel, Field

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid7()), frozen=True)
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    active: bool = Field(default=True)

class Address(BaseModel):
    street_address: str = Field(min_length=1)
    city: str = Field(min_length=1)
    postal_code: str = Field(min_length=1)
    label: str = Field(min_length=1) 

class Customer(User):
    role: Literal["customer"] = "customer"
    addresses: list[Address] = Field(default_factory=list)
    payment_method: str | None = Field(default=None, min_length=1)  # Unused for now

class RestaurantOwner(User):
    role: Literal["restaurant_owner"] = "restaurant_owner"
    restaurant_id: str = Field(min_length=1)

class Admin(User):
    role: Literal["admin"] = "admin"
    permissions: list[str] = Field(default_factory=list) # Unused for now

AnyUser = Annotated[Union[Customer, RestaurantOwner, Admin], Field(discriminator="role")]