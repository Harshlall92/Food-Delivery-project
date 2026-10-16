from pydantic_core import ValidationError
import pytest
import json
from unittest.mock import patch
from app.repositories.restaurant_repository import RestaurantRepository
from app.services.restaurant_service import *
from app.schemas.restaurant import Restaurant
from tests.util.helpers import *

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.mark.anyio
async def test_get_restaurants(tmp_path, mocker):
    mock_repository = create_restaurant_repository(create_restaurant_file(tmp_path))

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
    assert result[0].id == mock_data[0]["id"]
    assert result[0].name == mock_data[0]["name"]
    assert result[0].address == mock_data[0]["address"]
    assert result[0].cuisine == mock_data[0]["cuisine"]

    assert result[1].id == mock_data[1]["id"]
    assert result[1].name == mock_data[1]["name"]
    assert result[1].address == mock_data[1]["address"]
    assert result[1].cuisine == mock_data[1]["cuisine"]



@pytest.mark.anyio
async def test_get_restaurants_on_empty_data(tmp_path, mocker):

    mock_repository = create_restaurant_repository(create_restaurant_file(tmp_path))

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
    assert restaurant.id == "01a0fd78-2c5c-72f4-b913-672a802a7116"
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
async def test_create_restaurants(tmp_path):
    mock_repository = create_restaurant_repository(create_restaurant_file(tmp_path))

    data = RestaurantInput(name="Test Restaurant", address="123 Test St", cuisine="Italian")
    result = await create_restaurants(mock_repository, data)

    assert isinstance(result, Restaurant)
    assert result.name == "Test Restaurant"
    assert result.address == "123 Test St"
    assert result.cuisine == "Italian"

    contents = await mock_repository._read_file()

    assert len(contents) == 1

@pytest.mark.anyio
async def test_get_full_restaurant_info(tmp_path):
    restaurant_file = create_restaurant_file(tmp_path)
    restaurant_repository = create_restaurant_repository(restaurant_file)

    menu_items_file = create_menu_item_file(tmp_path)
    menu_item_repository = create_menu_item_repository(menu_items_file)

    restaurant_data = {
        "id": "01a0fd78-2c5c-72f4-b913-672a802a7116",
        "name": "Test Restaurant",
        "address": "123 Test St",
        "cuisine": "Italian"
    }

    restaurant_file.write_text(json.dumps([restaurant_data]))

    mock_menu_items = [
        {"id": "1", "restaurant_id": restaurant_data["id"], "name": "Pizza", "price": 10.99, "description": "Delicious pizza", "available": True},
        {"id": "2", "restaurant_id": restaurant_data["id"], "name": "Pasta", "price": 12.99, "description": "Tasty pasta", "available": True}
    ]

    menu_items_file.write_text(json.dumps(mock_menu_items))

    result = await get_full_restaurant_info(restaurant_repository, menu_item_repository, restaurant_data["id"])

    assert result is not None
    assert result.id == restaurant_data["id"]
    assert result.name == restaurant_data["name"]
    assert result.address == restaurant_data["address"]
    assert result.cuisine == restaurant_data["cuisine"]
    assert len(result.menu_items) == 2

@pytest.mark.anyio
async def test_get_full_restaurant_info_not_found(tmp_path):
    restaurant_file = create_restaurant_file(tmp_path)
    restaurant_repository = create_restaurant_repository(restaurant_file)

    menu_items_file = create_menu_item_file(tmp_path)
    menu_item_repository = create_menu_item_repository(menu_items_file)

    non_existent_id = "non-existent-id"

    with pytest.raises(mService.RestaurantNotFoundError):
        await get_full_restaurant_info(restaurant_repository, menu_item_repository, non_existent_id)
        