import json
from pydantic_core import ValidationError
import pytest
from unittest.mock import patch
from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.menu_item_repository import MenuItemRepository
from app.schemas.menu_item import MenuItemInput, MenuItem
from app.services.menu_item_service import *
from tests.util.helpers import *

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.mark.anyio
async def test_create_menu_item(tmp_path):
    restaurant_file = create_restaurant_file(tmp_path)
    menu_items_file = create_menu_item_file(tmp_path)

    restaurant_repository = create_restaurant_repository(restaurant_file)
    menu_item_repository = create_menu_item_repository(menu_items_file)
    
    restaurant_id = "01a0fd78-2c5c-72f4-b913-672a802a7116"
    restaurant_file_contents = [{"id": restaurant_id, "name": "Restaurant A", "address": "123 Main St", "cuisine": "Italian"}]
    restaurant_file.write_text(json.dumps(restaurant_file_contents))

    data = MenuItemInput(name="Test Item", price=9.99, description="Sample Description")

    result = await create_menu_item(
        restaurant_repository=restaurant_repository,
        menu_item_repository=menu_item_repository,
        restaurant_id=restaurant_id,
        data=data
    )

    assert result.restaurant_id == restaurant_id
    assert result.name == "Test Item"
    assert result.price == 9.99
    assert result.description == "Sample Description"
    assert result.available

    contents = json.loads(menu_items_file.read_text())
    assert len(contents) == 1

@pytest.mark.anyio
async def test_get_menu_items_by_restaurant_id(tmp_path):
    menu_items_file = create_menu_item_file(tmp_path)

    menu_item_repository = create_menu_item_repository(menu_items_file)

    restaurant_id = "01a0fd78-2c5c-72f4-b913-672a802a7116"

    menu_items_data = [
        {"id": "1", "restaurant_id": restaurant_id, "name": "Item 1", "price": 10.0, "description": "Desc 1", "available": True},
        {"id": "2", "restaurant_id": restaurant_id, "name": "Item 2", "price": 15.0, "description": "Desc 2", "available": True},
        {"id": "3", "restaurant_id": "other_restaurant", "name": "Item 3", "price": 20.0, "description": "Desc 3", "available": True}
    ]
    menu_items_file.write_text(json.dumps(menu_items_data))

    result = await get_menu_items_by_restaurant_id(menu_item_repository, restaurant_id)

    assert len(result) == 2
    assert result[0].name == "Item 1"
    assert result[1].name == "Item 2"

@pytest.mark.anyio
async def test_get_menu_items_by_restaurant_id_no_items(tmp_path):
    menu_items_file = create_menu_item_file(tmp_path)

    menu_item_repository = create_menu_item_repository(menu_items_file)

    restaurant_id = "01a0fd78-2c5c-72f4-b913-672a802a7116"

    menu_items_data = [
        {"id": "1", "restaurant_id": "other_restaurant", "name": "Item 1", "price": 10.0, "description": "Desc 1", "available": True},
        {"id": "2", "restaurant_id": "other_restaurant", "name": "Item 2", "price": 15.0, "description": "Desc 2", "available": True}
    ]

    menu_items_file.write_text(json.dumps(menu_items_data))

    result = await get_menu_items_by_restaurant_id(menu_item_repository, restaurant_id)

    assert len(result) == 0

@pytest.mark.anyio
async def test_validate_menu_item():
    menu_item_dict = {
        "id": "01a0fd78-2c5c-72f4-b913-672a802a71ff",
        "restaurant_id": "01a0fd78-2c5c-72f4-b913-672a802a7116",
        "name": "Item 1",
        "price": 10.0,
        "description": "Desc 1",
        "available": True
    }

    result = validate_menu_item(menu_item_dict)

    assert isinstance(result, MenuItemOutput)
    assert result.id == "01a0fd78-2c5c-72f4-b913-672a802a71ff"
    assert result.name == "Item 1"
    assert result.price == 10.0
    assert result.description == "Desc 1"

def test_validate_menu_item_with_invalid_types():
    menu_item_dict = {
        "id": "01a0fd78-2c5c-72f4-b913-672a802a71ff",
        "restaurant_id": "01a0fd78-2c5c-72f4-b913-672a802a7116",
        "name": "",
        "price": "invalid_price",
        "description": "",
        "available": True
    }

    with pytest.raises(ValidationError):
        validate_menu_item(menu_item_dict)

def test_validate_menu_item_with_missing_fields():
    menu_item_dict = {
        "id": "01a0fd78-2c5c-72f4-b913-672a802a71ff",
        "restaurant_id": "01a0fd78-2c5c-72f4-b913-672a802a7116",
        "name": "Item 1"
    }

    with pytest.raises(ValidationError):
        validate_menu_item(menu_item_dict)



