from fastapi.testclient import TestClient
import pytest

from app.main import app
from tests.util.fixtures import mocked_user_repository
from tests.util.builders import PASSWORD, create_test_customer

import app.services.authentication as auth
from tests.util.helpers import add_user_to_repository



client = TestClient(app)

class TestTokenEndpoint:

    def test_returns_bearer_token_for_valid_credentials(self, mocked_user_repository):
        customer = create_test_customer(password=PASSWORD)
        add_user_to_repository(customer)

        response = client.post(
            "/token",
            data={"username": customer.email, "password": PASSWORD},
        )

        assert response.status_code == 200
        assert response.json()["token_type"] == "bearer"
        assert auth.decode_token(response.json()["access_token"]) == customer.id

    @pytest.mark.parametrize(
        ("username", "password"),
        [
            ("missing@example.com", PASSWORD),
            ("customer@example.com", "wrong-password")
        ]
    )
    def test_rejects_invalid_credentials(self,mocked_user_repository, username, password):
        response = client.post(
            "/token",
            data={"username": username, "password": password}
        )

        assert response.status_code == 400
        assert response.json() == {"detail": "Incorrect email or password"}

    def test_rejects_missing_credentials(self):
        response = client.post(
            "/token",
            data={"username": "customer@example.com"}
        )

        assert response.status_code == 422
