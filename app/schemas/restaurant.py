from pydantic import BaseModel, Field
from uuid6 import uuid7

class Restaurant(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid7()), frozen=True) 
    name: str = Field(min_length=1)
    address: str = Field(min_length=1)
    cuisine: str = Field(min_length=1)
    active: bool = True

class RestaurantInput(BaseModel):
    name: str = Field(min_length=1) 
    address: str = Field(min_length=1)
    cuisine: str = Field(min_length=1)

class RestaurantOutput(BaseModel):
    id: str
    name: str
    address: str
    cuisine: str

class FullRestaurantOutput(RestaurantOutput):
    menu_items: list = []

class RestaurantUpdate(BaseModel):
    name: str | None = Field(default=None, min_length = 1)
    address: str | None = Field(default=None, min_length = 1)
    cuisine: str | None = Field(default=None, min_length = 1)
    active: bool | None = None
# Should probably add active fields to both output and update as well as validating list for full output