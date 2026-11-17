from fastapi.testclient import TestClient
from pytest import fail
from app.main import app

client = TestClient(app)

def create_test_file(tmp_path, monkeypatch):
    test_file = tmp_path / "users.json"
    test_file.write_text("[]")
    monkeypatch.setattr("app.repositories.user_repository.FILE_PATH", str(test_file))
    return test_file

def test_create_customer_account(tmp_path, monkeypatch):
    create_test_file(tmp_path, monkeypatch)
    payload = {
        "email": "test@example.com",
        "password": "testpw",
        "confirm_password": "testpw",
        "first_name": "Test",
        "last_name": "User"
    }

    response = client.post("/api/users/customers", json=payload)

    assert response.status_code == 201
