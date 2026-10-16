from unittest.mock import patch
from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.menu_item_repository import MenuItemRepository

def create_restaurant_file(tmp_path):
    restaurant_file = tmp_path / "restaurants.json"
    restaurant_file.write_text("[]")
    return restaurant_file

def create_restaurant_repository(restaurant_file):
    with patch("app.repositories.restaurant_repository.FILE_PATH", str(restaurant_file)):
        return RestaurantRepository()

def create_menu_item_file(tmp_path):
    menu_items_file = tmp_path / "menu-items.json"
    menu_items_file.write_text("[]")
    return menu_items_file

def create_menu_item_repository(menu_items_file):
    with patch("app.repositories.menu_item_repository.FILE_PATH", str(menu_items_file)):
        return MenuItemRepository()