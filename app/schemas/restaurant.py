from pydantic import BaseModel, Field
from uuid6 import uuid7

class Restaurant(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid7()), frozen=True) 

    name: str
    
    address: str
    
    cuisine: str

    active: bool = True
