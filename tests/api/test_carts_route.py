
import asyncio
from fastapi.testclient import TestClient
import pytest
from unittest.mock import AsyncMock
from app.main import app
from app.repositories.cart_repository import CartRepository
import app.api.routes.carts as carts_route
from tests.util.fixtures import mocked_cart_repository, mocked_user_repository 
from tests.api.test_users_route import create_test_user_create_dict
from tests.util.builders import create_test_cart


client = TestClient(app)

def create_test_cart_item(
    menu_item_id: str = "test_menu_item_id",
    quantity: int = 2,
    price_per_item: str = "10.00"
):
    return {
        "menu_item_id": menu_item_id,
        "quantity": quantity,
        "price_per_item": price_per_item
    }

def create_test_cart_create_dict(
    customer_id: str = "test_customer_id",
    menu_item_id: str = "test_menu_item_id",
    quantity = 2
):
    return {
        "customer_id": customer_id,
        "menu_item_id": menu_item_id,
        "quantity": quantity
    }

@pytest.fixture
def setup_test(mocked_cart_repository):
    pass


class TestDeleteCartEndpoint:

    def test_delete_cart_success_uses_repository(
        self, setup_test
    ):
        customer_id = "test_customer_id"
        asyncio.run(
            CartRepository().add_record(create_test_cart(customer_id=customer_id))
        )

        response = client.delete(f"/api/carts/{customer_id}")

        assert response.status_code == 204
        assert asyncio.run(CartRepository().get_all()) == []

    def test_delete_cart_not_found_uses_repository(self, setup_test):
        response = client.delete("/api/carts/nonexistent-id")

        assert response.status_code == 404
        assert response.json()["detail"] == (
            "Cart for customer with id nonexistent-id not found."
        )