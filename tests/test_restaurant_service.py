from pydantic_core import ValidationError
import pytest
from unittest.mock import AsyncMock, patch
from app.repositories.restaurant_repository import RestaurantRepository
from app.services.restaurant_service import *
from app.schemas.restaurant import Restaurant
from uuid6 import UUID

mock_repository = RestaurantRepository()

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.mark.anyio
async def test_get_restaurants(mocker):
    mock_data = [
        {"id": "01a0fd78-2c5c-72f4-b913-672a802a7116", "name": "Restaurant A", "address": "123 Main St", "cuisine": "Italian"},
        {"id": "01a0fd78-2c5d-735a-b1f3-b8c18b0d708a", "name": "Another Test", "address": "456 Oak Ave", "cuisine": "Mexican"}
    ]

    mocker.patch.object(
        mock_repository,
        "get_all",
        return_value=mock_data
    )
    
    result = await get_restaurants(mock_repository)

    assert len(result) == 2
    assert isinstance(result[0], Restaurant)
    assert isinstance(result[1], Restaurant)
    assert result[0].id == UUID(mock_data[0]["id"])
    assert result[0].name == mock_data[0]["name"]
    assert result[0].address == mock_data[0]["address"]
    assert result[0].cuisine == mock_data[0]["cuisine"]
    assert result[1].id == UUID(mock_data[1]["id"])
    assert result[1].name == mock_data[1]["name"]
    assert result[1].address == mock_data[1]["address"]
    assert result[1].cuisine == mock_data[1]["cuisine"]



@pytest.mark.anyio
async def test_get_restaurants_on_empty_data(mocker):

    mocker.patch.object(
        mock_repository,
        "get_all",
        return_value=[]
    )

    result = await get_restaurants(mock_repository)

    assert result == []

@pytest.mark.anyio
async def test_validate_restaurant():
    data = {"id": "01a0fd78-2c5c-72f4-b913-672a802a7116", "name": "Test Restaurant", "address": "123 Test St", "cuisine": "Italian"}

    restaurant = validate_restaurant(data)

    assert isinstance(restaurant, Restaurant)
    assert restaurant.id == UUID("01a0fd78-2c5c-72f4-b913-672a802a7116")
    assert restaurant.name == "Test Restaurant"
    assert restaurant.address == "123 Test St"
    assert restaurant.cuisine == "Italian"

@pytest.mark.anyio
async def test_validate_restaurant_with_missing_fields():
    data = {
        "id": "01a0fd78-2c5c-72f4-b913-672a802a7116",
        "name": "Test Restaurant"
    }

    try:
        validate_restaurant(data)
        assert False, "Expected a ValidationError due to missing fields"
    except ValidationError as e:
        assert True

@pytest.mark.anyio
async def test_validate_restaurant_with_extra_fields():
    data = {
        "id": "01a0fd78-2c5c-72f4-b913-672a802a7116",
        "name": "Test Restaurant",
        "address": "123 Test St",
        "cuisine": "Italian",
        "extra_field": "extra_value"
    }

    restaurant = validate_restaurant(data)

    # Asserting that the service does not raise an error and returns a Restaurant instance, ignoring the extra field

    assert isinstance(restaurant, Restaurant)

@pytest.mark.anyio
async def test_validate_restaurant_with_invalid_types():
    data = {
        "id": "01a0fd78-2c5c-72f4-b913-672a802a7116",
        "name": 123,
        "address": True,
        "cuisine": None
    }

    try:
        validate_restaurant(data)
        assert False, "Expected a ValidationError due to invalid types"
    except ValidationError as e:
        assert True

@pytest.mark.anyio
async def test_create_restaurants_valid():
    data = RestaurantInput(name = "place", address = "street", cuisine = "type", active = True)
    fake_data = {
        "id": "01a0fd78-2c5c-72f4-b913-672a802a7116",
        "name": "place",
        "address": "street",
        "cuisine": "type",
        "active" : True
    }

    with patch(
        "app.services.restaurant_service.RestaurantRepository.add_record",
        new_callable = AsyncMock,
        return_value = fake_data
    ):
        responce = await create_restaurants(RestaurantRepository,data)

    assert isinstance(responce, Restaurant)
    assert responce.name == "place"
    assert str(responce.id) == fake_data["id"]

@pytest.mark.anyio
async def test_create_restaurants_invalid_format():
    data = RestaurantInput(name = "place", address = "street", cuisine = "type", active = True)
    fake_data = {
        "id": "01a0fd78-2c5c-72f4-b913-672a802a7116",
        "name": True,
        "address": "type",
        "cuisine": "street",
        "active" : "place"
    }
    with patch(
        "app.services.restaurant_service.RestaurantRepository.add_record",
        new_callable = AsyncMock,
        return_value = fake_data
    ):
        try:
           await create_restaurants(RestaurantRepository,data)
        except ValueError:
           pass