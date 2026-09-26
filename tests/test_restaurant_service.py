import pytest
from unittest.mock import AsyncMock, patch
from app.services.restaurant_service import get_restaurants, validate_restaurant
from app.schemas.restaurant import Restaurant

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.mark.anyio
async def test_get_restaurant_valid_model():
    fake_data = [
        {"id" : 1, "name": "Place1", "address": "Street1", "category": "Type1",},
        {"id" : 2, "name": "Place2", "address": "Street2", "category": "Type2",},
    ]

    with patch(
        "app.services.restaurant_service.RestaurantRepository.get_restaurants",
        new_callable = AsyncMock,
        return_value = fake_data,
    ):
        result = await get_restaurants()
    assert len(result) == 2
    assert result[0].name == "Place1"

@pytest.mark.anyio
async def test_null_valid_model():
    fake_data = {"id" : 1, "name": None, "address": "Street1", "category": "Type1",}
    with pytest.raises(ValueError):
        validate_restaurant(fake_data)