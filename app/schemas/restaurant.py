from pydantic import UUID7, BaseModel, Field
from uuid6 import uuid7

class Restaurant(BaseModel):
    id: UUID7 = Field(default_factory=uuid7, frozen=True) 

    name: str = Field(min_length=1)
    
    address: str = Field(min_length=1)
    
    cuisine: str = Field(min_length=1)

    active: bool = True
