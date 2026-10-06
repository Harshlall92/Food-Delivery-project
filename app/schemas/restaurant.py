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
