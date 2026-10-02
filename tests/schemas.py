from pydantic import BaseModel

class TestModel(BaseModel):
    __test__ = False

    id: str
    name: str