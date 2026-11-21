import asyncio

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories.cart_repository import CartRepository
from tests.util.builders import create_test_cart
from tests.util.fixtures import mocked_cart_repository

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