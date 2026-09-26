import json
import pytest
from app.repositories.restaurant_repository import RestaurantRepository

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.mark.anyio
async def test_get_restaurant(tmp_path):
    data = [{
        "id" : 1, 
        "name" : "Place",
        "address": "Street",
        "category": "Type",
        "is_open" : "true",
    }]
    file_path = tmp_path / "restaurants.json"
    file_path.write_text(json.dumps(data), encoding = "utf-8")
    reop = RestaurantRepository(filepath=str(file_path))
    content = await reop.get_restaurants()
    assert content == data

@pytest.mark.anyio
async def test_get_restaurant_invalid_json(tmp_path):
    file_path = tmp_path / "wrong.json"
    file_path.write_text("{not valid json}", encoding = "utf-8")

    repo = RestaurantRepository(filepath = str(file_path))

    with pytest.raises(json.JSONDecodeError):
        await repo.get_restaurants()
    