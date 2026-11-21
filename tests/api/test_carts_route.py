import asyncio

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories.cart_repository import CartRepository
from tests.util.builders import create_test_cart
from tests.util.fixtures import mocked_cart_repository
from tests.util.helpers import create_test_customer
from app.repositories.user_repository import UserRepository
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.menu_item import MenuItem
from app.schemas.restaurant import Restaurant

client = TestClient(app)

CUSTOMER_ID = "01a1e9a4-021a-7f27-8546-c524b7f1ae7b"
MISSING_ID = "00000000-0000-0000-0000-000000000000"

@pytest.fixture
def setup_test(mocked_cart_repository):
    pass

class TestDeleteCartEndpoint:

    def test_delete_cart_full_workflow(self, setup_test):
        asyncio.run(CartRepository().add_record(create_test_cart(customer_id=CUSTOMER_ID)))

        response = client.delete(f"/api/carts/{CUSTOMER_ID}")
        assert response.status_code == 204
        assert response.content == b""
        assert asyncio.run(CartRepository().get_all()) == []

        # The cart is gone, so retrieving or deleting it again returns 404
        assert client.get(f"/api/carts/{CUSTOMER_ID}").status_code == 404
        assert client.delete(f"/api/carts/{CUSTOMER_ID}").status_code == 404

    def test_delete_cart_not_found_returns_404(self, setup_test):
        response = client.delete(f"/api/carts/{MISSING_ID}")

        assert response.status_code == 404
        assert response.json()["detail"] == f"Cart for customer with id {MISSING_ID} not found."



def create_test_cart_create_dict(customer_id, menu_item_id, quantity=1):
    return {"customer_id": customer_id, "menu_item_id": menu_item_id, "quantity": quantity}


@pytest.fixture
def cart_data(tmp_path, monkeypatch):
    # Point every repository the route uses at empty temporary files
    for name in ["cart.json", "users.json", "menu-items.json", "restaurants.json"]:
        (tmp_path / name).write_text("[]")
    monkeypatch.setattr("app.repositories.cart_repository.FILE_PATH", str(tmp_path / "cart.json"))
    monkeypatch.setattr("app.repositories.user_repository.FILE_PATH", str(tmp_path / "users.json"))
    monkeypatch.setattr("app.repositories.menu_item_repository.FILE_PATH", str(tmp_path / "menu-items.json"))
    monkeypatch.setattr("app.repositories.restaurant_repository.FILE_PATH", str(tmp_path / "restaurants.json"))

    customer = create_test_customer()
    restaurant = Restaurant(name="Test Restaurant", address="1 Main St", cuisine="thai")
    menu_item = MenuItem(restaurant_id=restaurant.id, name="Pad Thai", price=12.5)

    asyncio.run(UserRepository().add_record(customer))
    asyncio.run(RestaurantRepository().add_record(restaurant))
    asyncio.run(MenuItemRepository().add_record(menu_item))

    return {"customer": customer, "restaurant": restaurant, "menu_item": menu_item}


class TestCreateCartEndpoint:

    def test_create_cart(self, cart_data):
        payload = create_test_cart_create_dict(cart_data["customer"].id, cart_data["menu_item"].id, 2)

        response = client.post("/api/carts", json=payload)

        assert response.status_code == 201
        assert response.json()["subtotal"] == "25.00"

    def test_create_cart_invalid_quantity(self, cart_data):
        payload = create_test_cart_create_dict(cart_data["customer"].id, cart_data["menu_item"].id, 0)

        response = client.post("/api/carts", json=payload)

        assert response.status_code == 422

    def test_create_cart_customer_not_found(self, cart_data):
        payload = create_test_cart_create_dict("missing", cart_data["menu_item"].id)

        response = client.post("/api/carts", json=payload)

        assert response.status_code == 404

    def test_create_cart_inactive_customer(self, cart_data):
        inactive = create_test_customer(email="inactive@example.com")
        inactive.active = False
        asyncio.run(UserRepository().add_record(inactive))
        payload = create_test_cart_create_dict(inactive.id, cart_data["menu_item"].id)

        response = client.post("/api/carts", json=payload)

        assert response.status_code == 401

    def test_create_cart_duplicate(self, cart_data):
        payload = create_test_cart_create_dict(cart_data["customer"].id, cart_data["menu_item"].id)
        client.post("/api/carts", json=payload)

        response = client.post("/api/carts", json=payload)

        assert response.status_code == 409

    def test_create_cart_menu_item_not_found(self, cart_data):
        payload = create_test_cart_create_dict(cart_data["customer"].id, "missing")

        response = client.post("/api/carts", json=payload)

        assert response.status_code == 404

    def test_create_cart_menu_item_unavailable(self, cart_data):
        item = MenuItem(restaurant_id=cart_data["restaurant"].id, name="Green Curry", price=14.0, available=False)
        asyncio.run(MenuItemRepository().add_record(item))
        payload = create_test_cart_create_dict(cart_data["customer"].id, item.id)

        response = client.post("/api/carts", json=payload)

        assert response.status_code == 422