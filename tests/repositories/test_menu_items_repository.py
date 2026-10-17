import json
import pytest

from unittest.mock import patch
from app.repositories.menu_item_repository import MenuItemRepository, MenuItem

@pytest.fixture
def anyio_backend():
    return "asyncio"


def create_menu_items_file(tmp_path):
    file = tmp_path / "menu-items.json"
    file.write_text("[]")
    return file

def create_repository(file_path):
    with patch("app.repositories.menu_item_repository.FILE_PATH", str(file_path)):
        return MenuItemRepository()

@pytest.mark.anyio
async def test_get_menu_items_by_restaurant_id(tmp_path):
    menu_items_file = create_menu_items_file(tmp_path)
    repository = create_repository(menu_items_file)

    file_contents = [
        {
            "id": "1",
            "restaurant_id": "restaurant_1",
            "name": "Pizza",
            "price": 10.99,
            "description": "Delicious pizza",
            "available": True
        },
        {
            "id": "2",
            "restaurant_id": "restaurant_2",
            "name": "Burger",
            "price": 8.99,
            "description": "Juicy burger",
            "available": True
        },
        {
            "id": "3",
            "restaurant_id": "restaurant_1",
            "name": "Pasta",
            "price": 12.99,
            "description": "Tasty pasta",
            "available": True
        }
    ]

    menu_items_file.write_text(json.dumps(file_contents))

    result = await repository.get_menu_items_by_restaurant_id("restaurant_1")

    assert len(result) == 2

MENU_ITEMS_DATA = [
    {"id": "1", "restaurant_id": "restaurant_1", "name": "Pizza", "price": 10.99,
     "description": "Delicious pizza", "available": True},
    {"id": "2", "restaurant_id": "restaurant_2", "name": "Burger", "price": 8.99,
     "description": "Juicy burger", "available": True},
    {"id": "3", "restaurant_id": "restaurant_1", "name": "Pasta", "price": 12.99,
     "description": "Tasty pasta", "available": True},
]

@pytest.mark.anyio
async def test_update_record(tmp_path):
    menu_items_file = create_menu_items_file(tmp_path)
    repository = create_repository(menu_items_file)
    menu_items_file.write_text(json.dumps(MENU_ITEMS_DATA))
 
    updated = MenuItem(**{**MENU_ITEMS_DATA[0], "price": 14.5})
    result = await repository.update_record("1", updated)
 
    assert result["id"] == "1"
    assert result["price"] == 14.5
 
    contents = json.loads(menu_items_file.read_text())
    assert len(contents) == 3
    assert contents[0]["price"] == 14.5
    assert contents[0]["name"] == "Pizza"
    
@pytest.mark.anyio
async def test_update_record_not_found(tmp_path):
    menu_items_file = create_menu_items_file(tmp_path)
    repository = create_repository(menu_items_file)
    menu_items_file.write_text(json.dumps(MENU_ITEMS_DATA))
 
    missing = MenuItem(**{**MENU_ITEMS_DATA[0], "id": "unknown"})
    result = await repository.update_record("unknown", missing)
 
    assert result is None
    assert json.loads(menu_items_file.read_text()) == MENU_ITEMS_DATA
 