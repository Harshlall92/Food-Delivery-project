from pydantic_core import ValidationError
import pytest
from unittest.mock import patch
from app.repositories.restaurant_repository import RestaurantRepository
from app.services.restaurant_service import *
from app.schemas.restaurant import Restaurant

mock_repository = RestaurantRepository()

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.mark.anyio
async def test_get_restaurants(mocker):
    mock_data = [
        {"id": 1, "name": "Restaurant A", "address": "123 Main St", "category": "Italian"},
        {"id": 2, "name": "Another Test", "address": "456 Oak Ave", "category": "Mexican"}
    ]

    mocker.patch.object(
        mock_repository,
        "get_restaurants",
        return_value=mock_data
    )

    result = await get_restaurants(mock_repository)

    assert len(result) == 2
    assert isinstance(result[0], Restaurant)
    assert isinstance(result[1], Restaurant)
    assert result[0].id == 1
    assert result[0].name == "Restaurant A"
    assert result[0].address == "123 Main St"
    assert result[0].category == "Italian"
    assert result[1].id == 2
    assert result[1].name == "Another Test"
    assert result[1].address == "456 Oak Ave"
    assert result[1].category == "Mexican"



@pytest.mark.anyio
async def test_get_restaurants_on_empty_data(mocker):

    mocker.patch.object(
        mock_repository,
        "get_restaurants",
        return_value=[]
    )

    result = await get_restaurants(mock_repository)

    assert result == []

@pytest.mark.anyio
async def test_validate_restaurant():
    data = {"id": 1, "name": "Test Restaurant", "address": "123 Test St", "category": "Italian"}

    restaurant = validate_restaurant(data)

    assert isinstance(restaurant, Restaurant)
    assert restaurant.id == 1
    assert restaurant.name == "Test Restaurant"
    assert restaurant.address == "123 Test St"
    assert restaurant.category == "Italian"

@pytest.mark.anyio
async def test_validate_restaurant_with_missing_fields():
    data = {
        "id": 1,
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
        "id": 1,
        "name": "Test Restaurant",
        "address": "123 Test St",
        "category": "Italian",
        "extra_field": "extra_value"
    }

    restaurant = validate_restaurant(data)

    # Asserting that the service does not raise an error and returns a Restaurant instance, ignoring the extra field

    assert isinstance(restaurant, Restaurant)

@pytest.mark.anyio
async def test_validate_restaurant_with_invalid_types():
    data = {
        "id": "one",
        "name": 123,
        "address": True,
        "category": None
    }

    try:
        validate_restaurant(data)
        assert False, "Expected a ValidationError due to invalid types"
    except ValidationError as e:
        assert True