import json

from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.main import app
from app.schemas.restaurant import MenuItemInput


# Helper: makes empty temporary data files and tells the app to use them,
# so the tests never change the real files in the data/ folder.
def setup_test_files(tmp_path, monkeypatch):
    restaurants_file = tmp_path / "restaurants.json"
    menu_items_file = tmp_path / "menu_items.json"

    restaurants_file.write_text("[]")
    menu_items_file.write_text("[]")

    monkeypatch.setattr("app.repositories.restaurant_repository.FILE_PATH", str(restaurants_file))
    monkeypatch.setattr("app.repositories.menu_item_repository.FILE_PATH", str(menu_items_file))

    return menu_items_file


# Helper: creates a restaurant through the API and returns its id.
def create_test_restaurant(client):
    response = client.post(
        "/restaurants",
        json={"name": "Test Place", "address": "1 Main St", "cuisine": "Italian"},
    )
    return response.json()["id"]


def test_add_menu_item_works(tmp_path, monkeypatch):
    menu_items_file = setup_test_files(tmp_path, monkeypatch)
    client = TestClient(app)
    restaurant_id = create_test_restaurant(client)

    response = client.post(
        f"/restaurants/{restaurant_id}/menu-items",
        json={"name": "Margherita", "description": "Classic pizza", "price": 12.5},
    )

    # 201 means "created"
    assert response.status_code == 201

    item = response.json()
    assert item["name"] == "Margherita"
    assert item["price"] == 12.5
    assert item["restaurant_id"] == restaurant_id

    # Check the item was really saved in the file
    saved_items = json.loads(menu_items_file.read_text())
    assert len(saved_items) == 1


def test_add_menu_item_to_unknown_restaurant_gives_404(tmp_path, monkeypatch):
    menu_items_file = setup_test_files(tmp_path, monkeypatch)
    client = TestClient(app)

    response = client.post(
        "/restaurants/fake-id/menu-items",
        json={"name": "Margherita", "price": 12.5},
    )

    assert response.status_code == 404

    saved_items = json.loads(menu_items_file.read_text())
    assert len(saved_items) == 0


def test_add_menu_item_with_zero_price_gives_422(tmp_path, monkeypatch):
    menu_items_file = setup_test_files(tmp_path, monkeypatch)
    client = TestClient(app)
    restaurant_id = create_test_restaurant(client)

    response = client.post(
        f"/restaurants/{restaurant_id}/menu-items",
        json={"name": "Margherita", "price": 0},
    )

    # 422 means "the data you sent is invalid"
    assert response.status_code == 422

    saved_items = json.loads(menu_items_file.read_text())
    assert len(saved_items) == 0


def test_add_menu_item_with_negative_price_gives_422(tmp_path, monkeypatch):
    menu_items_file = setup_test_files(tmp_path, monkeypatch)
    client = TestClient(app)
    restaurant_id = create_test_restaurant(client)

    response = client.post(
        f"/restaurants/{restaurant_id}/menu-items",
        json={"name": "Margherita", "price": -5},
    )

    assert response.status_code == 422

    saved_items = json.loads(menu_items_file.read_text())
    assert len(saved_items) == 0