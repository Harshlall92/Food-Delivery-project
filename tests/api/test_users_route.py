from fastapi.testclient import TestClient
import pytest
from app.main import app

client = TestClient(app)

@pytest.fixture
def setup(tmp_path, monkeypatch):
    test_file = tmp_path / "users.json"
    test_file.write_text("[]")
    monkeypatch.setattr("app.repositories.user_repository.FILE_PATH", str(test_file))


def create_test_user_create_dict(
        email = "test@example.com",
        password = "testpw",
        confirm_password = "testpw",
        first_name = "Test",
        last_name = "User",
        ) -> dict:
    return {
        "email": email,
        "password": password,
        "confirm_password": confirm_password,
        "first_name": first_name,
        "last_name": last_name,
    }

class TestCustomerRoutes:

    def test_create_customer_account(self, setup):
        payload = create_test_user_create_dict()

        response = client.post("/api/users/c", json=payload)

        assert response.status_code == 201
        assert response.json()["email"] == payload["email"]

    def test_create_customer_account_duplicate_email(self, setup):
        payload = create_test_user_create_dict()

        client.post("/api/users/c", json=payload)

        response = client.post("/api/users/c", json=payload)

        assert response.status_code == 409
        assert response.json()["detail"] == f"Customer with email {payload['email']} already exists."

    def test_update_customer_account(self, setup):
        customer_id = client.post("/api/users/c", json=create_test_user_create_dict()).json()["id"]

        payload = {
            "email": "other@example.com",
            "password": "newpassword",
            "confirm_password": "newpassword",
            "first_name": "Tim",
            "last_name": "Apple",
            "active": False
        }

        response = client.patch(f"/api/users/c/{customer_id}", json=payload)

        assert response.status_code == 200
        assert response.json()["email"] == payload["email"]

    def test_update_customer_account_nonexistent_customer(self, setup):

        client.post("/api/users/c", json=create_test_user_create_dict())

        payload = {
            "email": "other@example.com"
        }

        response = client.patch("/api/users/c/nonexistent-id", json=payload)

        assert response.status_code == 404
        assert response.json()["detail"] == "Customer with ID nonexistent-id not found."

    def test_update_customer_account_duplicate_email(self, setup):
        customer = client.post("/api/users/c", json=create_test_user_create_dict())
        client.post("/api/users/c", json=create_test_user_create_dict(email="other@example.com"))

        payload = {
            "email": "other@example.com"
        }

        response = client.patch(f"/api/users/c/{customer.json()['id']}", json=payload)

        assert response.status_code == 409
        assert response.json()["detail"] == f"Customer with email {payload['email']} already exists."

class TestRestaurantOwnerRoutes:

    def test_create_restaurant_owner_account(self, setup):
        payload = create_test_user_create_dict()

        response = client.post("/api/users/r", json=payload)

        assert response.status_code == 201
        assert response.json()["email"] == payload["email"]

    def test_create_restaurant_owner_account_duplicate_email(self, setup):
        payload = create_test_user_create_dict()

        client.post("/api/users/r", json=payload)

        response = client.post("/api/users/r", json=payload)

        assert response.status_code == 409
        assert response.json()["detail"] == f"Restaurant owner with email {payload['email']} already exists."

    def test_create_restaurant_owner_account_invalid_input(self, setup):
        payload = create_test_user_create_dict(confirm_password="differentpw")

        response = client.post("/api/users/r", json=payload)

        assert response.status_code == 422
        assert "Passwords do not match." in response.json()["detail"][0]["msg"] 

    