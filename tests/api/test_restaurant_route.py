import json
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app.repositories.restaurant_repository import RestaurantRepository
from app.services.menu_item_service import RestaurantNotFoundError
from app.main import app
from app.schemas.restaurant import *
from tests.util.helpers import create_restaurant_file, create_restaurant_repository, create_menu_item_file, create_menu_item_repository


client = TestClient(app)

def test_get_restaurant():
    fake_data = [
        Restaurant(
            id = "01a0fd78-2c5c-72f4-b913-672a802a7116",
            name = "place",
            address = "street",
            cuisine = "type"
            ),
    ]
    with patch(
        "app.api.routes.restaurants.rService.get_restaurants",
        new_callable=AsyncMock,
        return_value = fake_data
    ):
        response = client.get("/api/restaurants")
    assert response.status_code == 200
    assert response.json() == [
        {"id" : "01a0fd78-2c5c-72f4-b913-672a802a7116", "name" : "place", "address" : "street", "cuisine" : "type","active":True}
    ]

def test_get_restaurant_fail():
    client = TestClient(app, raise_server_exceptions = False)
    with patch(
        "app.api.routes.restaurants.rService.get_restaurants",
        new_callable=AsyncMock,
        side_effect = ValueError(),
    ):
        response = client.get("/api/restaurants")
    assert response.status_code == 500

def test_create_restaurant_integrated(tmp_path):
    file_path = tmp_path / "test.json"
    with patch("app.repositories.restaurant_repository.FILE_PATH", str(file_path)):

        payload = {
            "name": "Test Restaurant",
            "address": "123 Test St",
            "cuisine": "Italian"
        }

        response = client.post("/api/restaurants", json=payload)

    assert response.status_code == 201
    response_data = response.json()

    assert response_data["name"] == "Test Restaurant"

    contents = file_path.read_text(encoding="utf-8")
    assert "Test Restaurant" in contents

def test_create_restaurant_fail():
    response = client.post("/api/restaurants", json = {"name": "place"})
    assert response.status_code == 422

def test_get_restaurant_by_id_integrated(tmp_path, monkeypatch):
    restaurant_file = create_restaurant_file(tmp_path)
    menu_items_file = create_menu_item_file(tmp_path)

    monkeypatch.setattr("app.repositories.restaurant_repository.FILE_PATH", str(restaurant_file))
    monkeypatch.setattr("app.repositories.menu_item_repository.FILE_PATH", str(menu_items_file))

    restaurant_id = "01a0fd78-2c5c-72f4-b913-672a802a7116"
    restaurant_data = {
        "id": restaurant_id,
        "name": "Test Restaurant",
        "address": "123 Test St",
        "cuisine": "Italian",
        "active": True
    }

    restaurant_file.write_text(json.dumps([restaurant_data]))

    menu_items_data = [
        {"id": "1", "restaurant_id": restaurant_id, "name": "Pizza", "price": 10.99, "description": "Delicious pizza", "available": True},
        {"id": "2", "restaurant_id": restaurant_id, "name": "Pasta", "price": 12.99, "description": "Tasty pasta", "available": True},
        {"id": "3", "restaurant_id": "other_restaurant", "name": "Burger", "price": 8.99, "description": "Juicy burger", "available": True}
    ]

    menu_items_file.write_text(json.dumps(menu_items_data))

    response = client.get(f"/api/restaurants/{restaurant_id}")

    assert response.status_code == 200
    response_data = response.json()

    assert response_data["id"] == restaurant_id
    assert response_data["name"] == "Test Restaurant"
    assert response_data["address"] == "123 Test St"
    assert response_data["cuisine"] == "Italian"
    assert len(response_data["menu_items"]) == 2

def test_get_restaurant_by_id_not_found():
    response = client.get("/api/restaurants/nonexistent-id")
    assert response.status_code == 404

RESTAURANT_ID = "01a0fd78-2c5c-72f4-b913-672a802a7116"
RESTAURANTS_DATA = [
    {"id": RESTAURANT_ID, "name": "Test Restaurant", "address": "123 Test St",
     "cuisine": "Italian", "active": True},
    {"id": "01a0fd78-2c5d-735a-b1f3-b8c18b0d708a", "name": "Another Test", "address": "456 Oak Ave",
     "cuisine": "Mexican", "active": True},
]
 
 
# Helper: points the app at a temp restaurants file filled with the sample data.
def setup_restaurant_file(tmp_path, monkeypatch):
    restaurant_file = create_restaurant_file(tmp_path)
    monkeypatch.setattr("app.repositories.restaurant_repository.FILE_PATH", str(restaurant_file))
    restaurant_file.write_text(json.dumps(RESTAURANTS_DATA))
    return restaurant_file

def test_update_restaurant(tmp_path, monkeypatch):
    restaurant_file = setup_restaurant_file(tmp_path, monkeypatch)
 
    response = client.patch(f"/api/restaurants/{RESTAURANT_ID}", json={"address": "newAddress"})
 
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == RESTAURANT_ID
    assert response_data["address"] == "newAddress"
    # Fields that were not sent stay the same
    assert response_data["name"] == "Test Restaurant"
    assert response_data["cuisine"] == "Italian"
 
    contents = json.loads(restaurant_file.read_text())
    assert len(contents) == 2
    assert contents[0]["address"] == "newAddress"
    assert contents[1] == RESTAURANTS_DATA[1]   # the other restaurant is untouched
 
def test_update_restaurant_wrong_type(tmp_path, monkeypatch):
    restaurant_file = setup_restaurant_file(tmp_path, monkeypatch)

    response = client.patch(f"/api/restaurants/{RESTAURANT_ID}", json={"cuisine": 123})

    assert response.status_code == 422
    assert json.loads(restaurant_file.read_text()) == RESTAURANTS_DATA
