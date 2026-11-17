from unittest.mock import patch
from app.schemas.user import Customer, RestaurantOwner
from app.repositories.user_repository import UserRepository
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

def create_user_file(tmp_path):
    user_file = tmp_path / "users.json"
    user_file.write_text("[]")
    return user_file

def create_user_repository(user_file):
    with patch("app.repositories.user_repository.FILE_PATH", str(user_file)):
        return UserRepository()

def create_test_customer(
        email = "test@example.com",
        password = "testpw",
        first_name = "Test",
        last_name = "User",
        addresses = [],
        payment_method = None
        ) -> Customer:
    return Customer(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        addresses=addresses,
        payment_method=payment_method
    )

def create_test_restaurant_owner(
        email: str = "test@example.com",
        password: str = "testpw",
        first_name: str = "Test",
        last_name: str = "User",
        restaurant_id: str | None = None
        ) -> RestaurantOwner:
    return RestaurantOwner(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        restaurant_id=restaurant_id
    )