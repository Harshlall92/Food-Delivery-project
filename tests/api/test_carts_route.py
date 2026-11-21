import asyncio

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories.cart_repository import CartRepository
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.user_repository import UserRepository
from app.schemas.menu_item import MenuItem
from app.schemas.restaurant import Restaurant
from tests.util.builders import create_test_cart
from tests.util.fixtures import (
    mocked_cart_repository, mocked_menu_item_repository,
    mocked_restaurant_repository, mocked_user_repository,
)
from tests.util.helpers import create_test_customer, create_test_restaurant_owner

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

@pytest.fixture
def create_cart_setup(mocked_cart_repository, mocked_user_repository,
                      mocked_restaurant_repository, mocked_menu_item_repository):
    customer = create_test_customer(email="customer@example.com")
    inactive_customer = create_test_customer(email="inactive@example.com").model_copy(update={"active": False})
    owner = create_test_restaurant_owner(email="owner@example.com")
    for user in (customer, inactive_customer, owner):
        asyncio.run(UserRepository().add_record(user))

    asyncio.run(RestaurantRepository().add_record(Restaurant(id="r1", name="Open", address="1 Main", cuisine="korean")))
    asyncio.run(MenuItemRepository().add_record(MenuItem(id="m1", restaurant_id="r1", name="Pizza", price=5.0)))
    asyncio.run(MenuItemRepository().add_record(MenuItem(id="m2", restaurant_id="r1", name="Soup", price=4.0, available=False)))

    return {"customer": customer.id, "inactive": inactive_customer.id, "owner": owner.id}


class TestCreateCartEndpoint:

    def test_create_cart_full_workflow(self, create_cart_setup):
        customer_id = create_cart_setup["customer"]

        response = client.post("/api/carts", json={"customer_id": customer_id, "menu_item_id": "m1", "quantity": 2})

        assert response.status_code == 201
        body = response.json()
        assert body["id"] == customer_id
        assert body["restaurant_id"] == "r1"
        assert body["items"] == [{"menu_item_id": "m1", "quantity": 2, "price": "5.00"}]
        assert body["subtotal"] == "10.00"

        cart = client.get(f"/api/carts/{customer_id}").json()
        assert cart["restaurant_name"] == "Open"
        assert cart["total_quantity"] == 2

    def test_create_cart_invalid_request_returns_422(self, create_cart_setup):
        customer_id = create_cart_setup["customer"]

        assert client.post("/api/carts", json={"menu_item_id": "m1"}).status_code == 422
        assert client.post("/api/carts", json={"customer_id": "", "menu_item_id": "m1"}).status_code == 422
        assert client.post("/api/carts", json={"customer_id": customer_id, "menu_item_id": "m1", "quantity": 0}).status_code == 422

    def test_create_cart_unknown_customer_returns_401(self, create_cart_setup):
        response = client.post("/api/carts", json={"customer_id": "missing", "menu_item_id": "m1"})
        assert response.status_code == 401

    def test_create_cart_not_a_customer_returns_401(self, create_cart_setup):
        response = client.post("/api/carts", json={"customer_id": create_cart_setup["owner"], "menu_item_id": "m1"})
        assert response.status_code == 401

    def test_create_cart_inactive_customer_returns_401(self, create_cart_setup):
        response = client.post("/api/carts", json={"customer_id": create_cart_setup["inactive"], "menu_item_id": "m1"})
        assert response.status_code == 401

    def test_create_cart_duplicate_returns_409(self, create_cart_setup):
        payload = {"customer_id": create_cart_setup["customer"], "menu_item_id": "m1"}

        assert client.post("/api/carts", json=payload).status_code == 201
        assert client.post("/api/carts", json=payload).status_code == 409

    def test_create_cart_menu_item_not_found_returns_404(self, create_cart_setup):
        response = client.post("/api/carts", json={"customer_id": create_cart_setup["customer"], "menu_item_id": "missing"})
        assert response.status_code == 404

    def test_create_cart_inactive_menu_item_returns_422(self, create_cart_setup):
        response = client.post("/api/carts", json={"customer_id": create_cart_setup["customer"], "menu_item_id": "m2"})
        assert response.status_code == 422
        assert "not available" in response.json()["detail"]