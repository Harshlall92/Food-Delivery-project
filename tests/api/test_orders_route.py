import asyncio

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories.cart_repository import CartRepository
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.order_item_repository import OrderItemRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.user_repository import UserRepository
from app.schemas.menu_item import MenuItem
from app.schemas.restaurant import Restaurant
from app.repositories.order_repository import OrderRepository
from tests.util.builders import create_test_cart, create_test_cart_item, create_test_order
from tests.util.fixtures import (
    mocked_cart_repository, mocked_menu_item_repository, mocked_order_item_repository,
    mocked_order_repository, mocked_restaurant_repository, mocked_user_repository,
)
from tests.util.helpers import create_test_customer, create_test_restaurant_owner

client = TestClient(app)


@pytest.fixture
def checkout_setup(mocked_order_repository, mocked_order_item_repository, mocked_cart_repository,
                   mocked_user_repository, mocked_restaurant_repository, mocked_menu_item_repository):
    customer = create_test_customer(email="customer@example.com")
    inactive_customer = create_test_customer(email="inactive@example.com").model_copy(update={"active": False})
    owner = create_test_restaurant_owner(email="owner@example.com")
    for user in (customer, inactive_customer, owner):
        asyncio.run(UserRepository().add_record(user))

    asyncio.run(RestaurantRepository().add_record(Restaurant(id="r1", name="Open", address="1 Main", cuisine="korean")))
    asyncio.run(RestaurantRepository().add_record(Restaurant(id="r2", name="Closed", address="2 Main", cuisine="thai", active=False)))
    for menu_item in (
        MenuItem(id="m1", restaurant_id="r1", name="Pizza", price=5.0),
        MenuItem(id="m3", restaurant_id="r1", name="Soup", price=4.0, available=False),
        MenuItem(id="m4", restaurant_id="r2", name="Curry", price=9.0),
    ):
        asyncio.run(MenuItemRepository().add_record(menu_item))

    return {"customer": customer.id, "inactive": inactive_customer.id, "owner": owner.id}


def add_cart(customer_id, restaurant_id="r1", menu_item_id="m1", items=None):
    if items is None:
        items = [create_test_cart_item(menu_item_id=menu_item_id, quantity=2, price="4.00")]
    asyncio.run(CartRepository().add_record(create_test_cart(customer_id=customer_id, restaurant_id=restaurant_id, items=items)))


class TestCheckoutEndpoint:

    def test_checkout_full_workflow(self, checkout_setup):
        customer_id = checkout_setup["customer"]
        add_cart(customer_id)

        response = client.post("/api/orders", json={"customer_id": customer_id})

        assert response.status_code == 201
        body = response.json()
        assert body["customer_id"] == customer_id
        assert body["restaurant_id"] == "r1"
        assert body["status"] == "pending"
        assert body["total"] == "10.00"

        items = asyncio.run(OrderItemRepository().get_items_by_order_id(body["id"]))
        assert [(i.menu_item_id, i.quantity, str(i.price_per_item)) for i in items] == [("m1", 2, "5.00")]

        assert client.get(f"/api/carts/{customer_id}").status_code == 404

    def test_checkout_invalid_request_returns_422(self, checkout_setup):
        assert client.post("/api/orders", json={}).status_code == 422
        assert client.post("/api/orders", json={"customer_id": 123}).status_code == 422

    def test_checkout_unknown_customer_returns_404(self, checkout_setup):
        assert client.post("/api/orders", json={"customer_id": "missing"}).status_code == 404

    def test_checkout_inactive_customer_returns_404(self, checkout_setup):
        add_cart(checkout_setup["inactive"])
        assert client.post("/api/orders", json={"customer_id": checkout_setup["inactive"]}).status_code == 404

    def test_checkout_not_a_customer_returns_404(self, checkout_setup):
        assert client.post("/api/orders", json={"customer_id": checkout_setup["owner"]}).status_code == 404

    def test_checkout_without_cart_returns_404(self, checkout_setup):
        assert client.post("/api/orders", json={"customer_id": checkout_setup["customer"]}).status_code == 404

    def test_checkout_empty_cart_returns_422(self, checkout_setup):
        add_cart(checkout_setup["customer"], items=[])
        assert client.post("/api/orders", json={"customer_id": checkout_setup["customer"]}).status_code == 422

    def test_checkout_inactive_restaurant_returns_422(self, checkout_setup):
        add_cart(checkout_setup["customer"], restaurant_id="r2", menu_item_id="m4")
        assert client.post("/api/orders", json={"customer_id": checkout_setup["customer"]}).status_code == 422

    def test_checkout_missing_menu_item_returns_422(self, checkout_setup):
        add_cart(checkout_setup["customer"], menu_item_id="missing")
        assert client.post("/api/orders", json={"customer_id": checkout_setup["customer"]}).status_code == 422

    def test_checkout_inactive_menu_item_returns_422(self, checkout_setup):
        add_cart(checkout_setup["customer"], menu_item_id="m3")
        assert client.post("/api/orders", json={"customer_id": checkout_setup["customer"]}).status_code == 422

    def test_checkout_menu_item_from_another_restaurant_returns_409(self, checkout_setup):
        add_cart(checkout_setup["customer"], menu_item_id="m4")
        assert client.post("/api/orders", json={"customer_id": checkout_setup["customer"]}).status_code == 409

    @pytest.fixture
    def existing_order(mocked_order_repository):
        order = create_test_order()
        asyncio.run(OrderRepository().add_record(order))
        return order


class TestUpdateOrderStatusEndpoint:

    def test_update_status_success(self, existing_order):
        response = client.patch(f"/api/orders/{existing_order.id}/status", json={"status": "ready"})

        assert response.status_code == 200
        body = response.json()
        assert body["id"] == existing_order.id
        assert body["status"] == "ready"
        assert asyncio.run(OrderRepository().get_by_id(existing_order.id)).status == "ready"

    @pytest.mark.parametrize("new_status", ["pending", "confirmed", "preparing", "ready", "picked up", "delivered", "cancelled"])
    def test_update_status_every_allowed_status(self, existing_order, new_status):
        response = client.patch(f"/api/orders/{existing_order.id}/status", json={"status": new_status})

        assert response.status_code == 200
        assert response.json()["status"] == new_status

    def test_update_status_malformed_request_returns_422(self, existing_order):
        url = f"/api/orders/{existing_order.id}/status"

        assert client.patch(url, json={}).status_code == 422
        assert client.patch(url, json={"status": 5}).status_code == 422
        assert client.patch(url, content="not json", headers={"Content-Type": "application/json"}).status_code == 422

    @pytest.mark.parametrize("bad_status", ["shipped", "Pending", "picked_up", ""])
    def test_update_status_invalid_value_returns_422(self, existing_order, bad_status):
        response = client.patch(f"/api/orders/{existing_order.id}/status", json={"status": bad_status})

        assert response.status_code == 422
        assert asyncio.run(OrderRepository().get_by_id(existing_order.id)).status == "pending"

    def test_update_status_missing_order_returns_404(self, mocked_order_repository):
        response = client.patch("/api/orders/missing/status", json={"status": "ready"})

        assert response.status_code == 404
        assert response.json()["detail"] == "Order with id missing not found."