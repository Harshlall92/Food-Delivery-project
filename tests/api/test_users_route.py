from fastapi.testclient import TestClient
from app.main import app

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

def create_test_file(tmp_path, monkeypatch):
    test_file = tmp_path / "users.json"
    test_file.write_text("[]")
    monkeypatch.setattr("app.repositories.user_repository.FILE_PATH", str(test_file))
    return test_file

def test_create_customer_account(tmp_path, monkeypatch):
    create_test_file(tmp_path, monkeypatch)
    payload = create_test_user_create_dict()

    response = client.post("/api/users/c", json=payload)

    assert response.status_code == 201
    assert response.json()["email"] == payload["email"]

def test_create_customer_account_duplicate_email(tmp_path, monkeypatch):
    create_test_file(tmp_path, monkeypatch)
    payload = create_test_user_create_dict()

    client.post("/api/users/c", json=payload)

    response = client.post("/api/users/c", json=payload)

    assert response.status_code == 409
    assert response.json()["detail"] == f"Customer with email {payload['email']} already exists."

def test_update_customer_account(tmp_path, monkeypatch):
    create_test_file(tmp_path, monkeypatch)
    client.post("/api/users/c", json=create_test_user_create_dict())

    payload = {
        "email": "other@example.com",
        "password": "newpassword",
        "confirm_password": "newpassword",
        "first_name": "Tim",
        "last_name": "Apple",
        "active": False
    }

    response = client.patch("/c", json=payload)

    assert response.status_code == 200
    assert response.json()["email"] == payload["email"]

def test_update_customer_account_nonexistent_customer(tmp_path, monkeypatch):
    create_test_file(tmp_path, monkeypatch)

    client.post("/api/users/c", json=create_test_user_create_dict())

    payload = {
        "email": "other@example.com"
    }

    response = client.patch("/api/users/c/nonexistent-id", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Customer with ID nonexistent-id not found."

def test_update_customer_account_duplicate_email(tmp_path, monkeypatch):
    create_test_file(tmp_path, monkeypatch)

    customer = client.post("/api/users/c", json=create_test_user_create_dict())
    client.post("/api/users/c", json=create_test_user_create_dict(email="other@example.com"))

    payload = {
        "email": "other@example.com"
    }

    response = client.patch(f"/api/users/c/{customer.json()['id']}", json=payload)

    assert response.status_code == 409
    assert response.json()["detail"] == f"Customer with email {payload['email']} already exists."
