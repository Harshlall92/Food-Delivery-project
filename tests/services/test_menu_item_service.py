import json
import pytest
from unittest.mock import patch
from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.menu_item_repository import MenuItemRepository
from app.schemas.restaurant import MenuItemInput, MenuItem
from app.services.menu_Item_service import *


def create_restaurant_file(tmp_path):
    restaurant_file = tmp_path / "restaurants.json"
    restaurant_file.write_text("[]")
    return restaurant_file

def create_menu_item_file(tmp_path):
    menu_items_file = tmp_path / "menu_items.json"
    menu_items_file.write_text("[]")
    return menu_items_file

def create_restaurant_repository(restaurant_file):
    with patch("app.repositories.restaurant_repository.FILE_PATH", str(restaurant_file)):
        return RestaurantRepository()

def create_menu_item_repository(menu_items_file):
    with patch("app.repositories.menu_item_repository.FILE_PATH", str(menu_items_file)):
        return MenuItemRepository()

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
    
