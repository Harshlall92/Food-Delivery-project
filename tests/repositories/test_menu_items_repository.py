import json
import pytest

from unittest.mock import patch
from app.repositories.menu_item_repository import MenuItemRepository

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

    