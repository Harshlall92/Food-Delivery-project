import pytest

from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.user_repository import UserRepository
from app.repositories.cart_repository import CartRepository
from tests.util.helpers import *

@pytest.fixture
def anyio_backend():
    return 'asyncio'

@pytest.fixture
def restaurant_repository(tmp_path) -> RestaurantRepository:
    return create_restaurant_repository(create_restaurant_file(tmp_path))

@pytest.fixture
def user_repository(tmp_path) -> UserRepository:
    return create_user_repository(create_user_file(tmp_path))

@pytest.fixture
def cart_repository(tmp_path) -> CartRepository:
    return create_cart_repository(create_cart_file(tmp_path))


@pytest.fixture
def mocked_user_repository(tmp_path, monkeypatch):
    user_file = create_user_file(tmp_path)

    monkeypatch.setattr("app.repositories.user_repository.FILE_PATH", str(user_file))

@pytest.fixture
def mocked_restaurant_repository(tmp_path, monkeypatch):
    restaurant_file = create_restaurant_file(tmp_path)

    monkeypatch.setattr("app.repositories.restaurant_repository.FILE_PATH", str(restaurant_file))

@pytest.fixture
def mocked_cart_repository(tmp_path, monkeypatch):
    cart_file = create_cart_file(tmp_path)

    monkeypatch.setattr("app.repositories.cart_repository.FILE_PATH", str(cart_file))