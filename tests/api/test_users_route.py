from fastapi.testclient import TestClient
import pytest
from app.main import app
from tests.util.fixtures import mocked_user_repository, mocked_restaurant_repository

client = TestClient(app)

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

    class TestCreateCustomerEndpoint:

        def test_create_customer_account(self, mocked_user_repository):
            payload = create_test_user_create_dict()

            response = client.post("/api/users/c", json=payload)

            assert response.status_code == 201
            assert response.json()["email"] == payload["email"]

        def test_create_customer_account_duplicate_email(self, mocked_user_repository):
            payload = create_test_user_create_dict()

            client.post("/api/users/c", json=payload)

            response = client.post("/api/users/c", json=payload)

            assert response.status_code == 409
            assert response.json()["detail"] == f"Customer with email {payload['email']} already exists."

        def test_create_customer_account_invalid_input(self, mocked_user_repository):
            payload = create_test_user_create_dict(confirm_password="differentpw")

            response = client.post("/api/users/c", json=payload)

            assert response.status_code == 422
            assert "Passwords do not match" in response.json()["detail"][0]["msg"]

    class TestUpdateCustomerEndpoint:

        def test_update_customer_account(self, mocked_user_repository):
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

        def test_update_customer_account_nonexistent_customer(self, mocked_user_repository):

            client.post("/api/users/c", json=create_test_user_create_dict())

            payload = {
                "email": "other@example.com"
            }

            response = client.patch("/api/users/c/nonexistent-id", json=payload)

            assert response.status_code == 404
            assert response.json()["detail"] == "Customer with ID nonexistent-id not found."

        def test_update_customer_account_duplicate_email(self, mocked_user_repository):
            customer = client.post("/api/users/c", json=create_test_user_create_dict())
            client.post("/api/users/c", json=create_test_user_create_dict(email="other@example.com"))

            payload = {
                "email": "other@example.com"
            }

            response = client.patch(f"/api/users/c/{customer.json()['id']}", json=payload)

            assert response.status_code == 409
            assert response.json()["detail"] == f"Customer with email {payload['email']} already exists."

        def test_update_customer_account_invalid_input(self, mocked_user_repository):
            customer = client.post("/api/users/c", json=create_test_user_create_dict())

            payload = {
                "password": "newpassword",
                "confirm_password": "differentpassword"
            }

            response = client.patch(f"/api/users/c/{customer.json()['id']}", json=payload)

            assert response.status_code == 422
            assert "Passwords do not match" in response.json()["detail"][0]["msg"]
    
    class TestAddCustomerAddressEndpoint:

        def test_add_address_to_customer(self, mocked_user_repository):
            customer_id = client.post("/api/users/c", json=create_test_user_create_dict()).json()["id"]

            address_payload = {
                "label": "Home",
                "address_line_1": "123 Main St",
                "city": "Testville",
                "province": "BC",
                "postal_code": "A1A 1A1"
            }

            response = client.post(f"/api/users/c/{customer_id}", json=address_payload)

            assert response.status_code == 200
            assert any(addr["label"] == address_payload["label"] for addr in response.json()["addresses"])

        def test_add_address_to_nonexistent_customer(self, mocked_user_repository):
            address_payload = {
                "label": "Home",
                "address_line_1": "123 Main St",
                "city": "Testville",
                "province": "BC",
                "postal_code": "A1A 1A1"
            }

            response = client.post("/api/users/c/nonexistent-id", json=address_payload)

            assert response.status_code == 404
            assert response.json()["detail"] == "Customer with ID nonexistent-id not found."

        def test_add_duplicate_address_label_to_customer(self, mocked_user_repository):
            customer_id = client.post("/api/users/c", json=create_test_user_create_dict()).json()["id"]

            address_payload = {
                "label": "Home",
                "address_line_1": "123 Main St",
                "city": "Testville",
                "province": "BC",
                "postal_code": "A1A 1A1"
            }

            client.post(f"/api/users/c/{customer_id}", json=address_payload)

            response = client.post(f"/api/users/c/{customer_id}", json=address_payload)

            assert response.status_code == 409
            assert response.json()["detail"] == f"Address with label {address_payload['label']} already exists for this customer."

        def test_add_address_to_non_customer(self, mocked_user_repository):
            restaurant_owner_id = client.post("/api/users/r", json=create_test_user_create_dict()).json()["id"]

            address_payload = {
                "label": "Home",
                "address_line_1": "123 Main St",
                "city": "Testville",
                "province": "BC",
                "postal_code": "A1A 1A1"
            }

            response = client.post(f"/api/users/c/{restaurant_owner_id}", json=address_payload)

            assert response.status_code == 422
            assert f"User with ID {restaurant_owner_id} is not a customer." in response.json()["detail"]

        def test_add_address_invalid_input(self, mocked_user_repository):
            customer_id = client.post("/api/users/c", json=create_test_user_create_dict()).json()["id"]

            address_payload = {
                "label": "Home",
                "address_line_1": "",
                "city": "Testville",
                "province": "BC",
                "postal_code": "A1A 1A1"
            }

            response = client.post(f"/api/users/c/{customer_id}", json=address_payload)

            assert response.status_code == 422
            assert any("Field cannot be empty" in err["msg"] for err in response.json()["detail"])

    class TestUpdateCustomerAddressEndpoint:

        def test_update_address_for_customer(self, mocked_user_repository):
            customer_id = client.post("/api/users/c", json=create_test_user_create_dict()).json()["id"]

            address_payload = {
                "label": "Home",
                "address_line_1": "123 Main St",
                "city": "Testville",
                "province": "BC",
                "postal_code": "A1A 1A1"
            }

            client.post(f"/api/users/c/{customer_id}", json=address_payload)

            updated_address_payload = {
                "label": "Work",
                "address_line_1": "456 Elm St",
                "city": "Newville",
                "province": "ON",
                "postal_code": "B2B 2B2"
            }

            response = client.patch(f"/api/users/c/{customer_id}/addresses/{address_payload['label']}", json=updated_address_payload)

            assert response.status_code == 200
            assert any(addr["address_line_1"] == updated_address_payload["address_line_1"] for addr in response.json()["addresses"])

        def test_update_address_for_nonexistent_customer(self, mocked_user_repository):
            address_payload = {
                "label": "Home",
                "address_line_1": "123 Main St",
                "city": "Testville",
                "province": "BC",
                "postal_code": "A1A 1A1"
            }

            response = client.patch("/api/users/c/nonexistent-id/addresses/Home", json=address_payload)

            assert response.status_code == 404
            assert response.json()["detail"] == "Customer with ID nonexistent-id not found."

        def test_update_nonexistent_address_for_customer(self, mocked_user_repository):
            customer_id = client.post("/api/users/c", json=create_test_user_create_dict()).json()["id"]

            address_payload = {
                "label": "Home",
                "address_line_1": "123 Main St",
                "city": "Testville",
                "province": "BC",
                "postal_code": "A1A 1A1"
            }

            response = client.patch(f"/api/users/c/{customer_id}/addresses/NonexistentLabel", json=address_payload)

            assert response.status_code == 404
            assert response.json()["detail"] == f"Address with label NonexistentLabel not found for this customer."

        def test_update_address_for_non_customer(self, mocked_user_repository):
            restaurant_owner_id = client.post("/api/users/r", json=create_test_user_create_dict()).json()["id"]

            address_payload = {
                "label": "Home",
                "address_line_1": "123 Main St",
                "city": "Testville",
                "province": "BC",
                "postal_code": "A1A 1A1"
            }

            response = client.patch(f"/api/users/c/{restaurant_owner_id}/addresses/Home", json=address_payload)

            assert response.status_code == 422
            assert f"User with ID {restaurant_owner_id} is not a customer." in response.json()["detail"]

        def test_update_address_invalid_input(self, mocked_user_repository):
            customer_id = client.post("/api/users/c", json=create_test_user_create_dict()).json()["id"]

            address_payload = {
                "label": "Home",
                "address_line_1": "123 Main St",
                "city": "Testville",
                "province": "BC",
                "postal_code": "A1A 1A1"
            }

            client.post(f"/api/users/c/{customer_id}", json=address_payload)

            updated_address_payload = {
                "label": "Work",
                "address_line_1": "",
                "city": "Newville",
                "province": "ON",
                "postal_code": "B2B 2B2"
            }

            response = client.patch(f"/api/users/c/{customer_id}/addresses/{address_payload['label']}", json=updated_address_payload)

            assert response.status_code == 422
            assert any("Field cannot be empty" in err["msg"] for err in response.json()["detail"])

class TestRestaurantOwnerRoutes:

    class TestCreateRestaurantOwnerEndpoint:

        def test_create_restaurant_owner_account(self, mocked_user_repository):
            payload = create_test_user_create_dict()

            response = client.post("/api/users/r", json=payload)

            assert response.status_code == 201
            assert response.json()["email"] == payload["email"]

        def test_create_restaurant_owner_account_duplicate_email(self, mocked_user_repository):
            payload = create_test_user_create_dict()

            client.post("/api/users/r", json=payload)

            response = client.post("/api/users/r", json=payload)

            assert response.status_code == 409
            assert response.json()["detail"] == f"Restaurant owner with email {payload['email']} already exists."

        def test_create_restaurant_owner_account_invalid_input(self, mocked_user_repository):
            payload = create_test_user_create_dict(confirm_password="differentpw")

            response = client.post("/api/users/r", json=payload)

            assert response.status_code == 422
            assert "Passwords do not match" in response.json()["detail"][0]["msg"] 

    class TestUpdateRestaurantOwnerEndpoint:

        def test_update_restaurant_owner(self, mocked_user_repository, mocked_restaurant_repository):
            customer_id = client.post("/api/users/r", json=create_test_user_create_dict()).json()["id"]
            restaurant_data = {
                "name": "Test Restaurant",
                "address": "123 Test St",
                "cuisine": "Test Cuisine"
            }
            restaurant_response = client.post("/api/restaurants", json=restaurant_data)

            assert restaurant_response.status_code == 201

            restaurant_id = restaurant_response.json()["id"]

            update_payload = {
                "restaurant_id": restaurant_id
            }

            response = client.patch(f"/api/users/r/{customer_id}", json=update_payload)

            assert response.status_code == 200
            assert response.json()["restaurant_id"] == restaurant_id

        def test_update_restaurant_owner_nonexistent_restaurant(self, mocked_user_repository, mocked_restaurant_repository):
            owner_id = client.post("/api/users/r", json=create_test_user_create_dict()).json()["id"]

            update_payload = {
                "restaurant_id": "nonexistent-restaurant-id"
            }

            response = client.patch(f"/api/users/r/{owner_id}", json=update_payload)

            assert response.status_code == 404
            assert "Restaurant with ID nonexistent-restaurant-id does not exist." in response.json()["detail"]

        def test_update_restaurant_owner_nonexistent_user(self, mocked_user_repository, mocked_restaurant_repository):
            update_payload = {
                "restaurant_id": "some-restaurant-id"
            }

            response = client.patch("/api/users/r/nonexistent-user-id", json=update_payload)

            assert response.status_code == 404
            assert "Restaurant owner with ID nonexistent-user-id not found." in response.json()["detail"]

        def test_update_restaurant_owner_duplicate_email(self, mocked_user_repository, mocked_restaurant_repository):
            restaurant_owner = client.post("/api/users/r", json=create_test_user_create_dict()).json()["id"]
            update_email = "other@example.com"
            client.post("/api/users/r", json=create_test_user_create_dict(email=update_email))

            update_payload = {
                "email": update_email
            }

            response = client.patch(f"/api/users/r/{restaurant_owner}", json=update_payload)

            assert response.status_code == 409
            assert response.json()["detail"] == f"Restaurant owner with email {update_email} already exists."

        def test_update_restaurant_owner_invalid_input(self, mocked_user_repository, mocked_restaurant_repository):
            restaurant_owner = client.post("/api/users/r", json=create_test_user_create_dict()).json()["id"]

            update_payload = {
                "password": "newpassword",
                "confirm_password": "differentpassword"
            }

            response = client.patch(f"/api/users/r/{restaurant_owner}", json=update_payload)

            assert response.status_code == 422
            assert "Passwords do not match" in response.json()["detail"][0]["msg"]
