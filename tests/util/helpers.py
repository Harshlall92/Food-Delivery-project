from unittest.mock import patch

import jwt
from datetime import datetime, timedelta, UTC
from fastapi.security import OAuth2PasswordRequestForm

from app.services.authentication import SECRET_KEY, ALGORITHM
from app.schemas.user import AnyUser, Customer, RestaurantOwner
from app.repositories.user_repository import UserRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.cart_repository import CartRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.order_item_repository import OrderItemRepository

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

def create_cart_file(tmp_path):
    cart_file = tmp_path / "cart.json"
    cart_file.write_text("[]")
    return cart_file

def create_cart_repository(cart_file):
    with patch("app.repositories.cart_repository.FILE_PATH", str(cart_file)):
        return CartRepository()

def create_order_file(tmp_path):
    order_file = tmp_path / "orders.py"
    order_file.write_text("[]")
    return order_file

def create_order_repository(order_file):
    with patch("app.repositories.order_repository.FILE_PATH", str(order_file)):
        return OrderRepository()

def create_order_item_file(tmp_path):
    order_item_file = tmp_path / "order-items.py"
    order_item_file.write_text("[]")
    return order_item_file

def create_order_item_repository(order_item_file):
    with patch("app.repositories.order_item_repository.FILE_PATH", str(order_item_file)):
        return OrderItemRepository()

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

def credentials(username: str, password: str):
    return OAuth2PasswordRequestForm(username=username, password=password)

def token_for(user_id: str, *, secret=None, expires=None) -> str:
    return jwt.encode(
        {"sub": user_id, "exp": expires or datetime.now(UTC) + timedelta(minutes=5)},
        secret or SECRET_KEY,
        algorithm=ALGORITHM
    )
