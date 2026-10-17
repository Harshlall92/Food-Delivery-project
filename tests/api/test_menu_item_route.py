import json

from fastapi.testclient import TestClient

from app.main import app


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
        "/api/restaurants",
        json={"name": "Test Place", "address": "1 Main St", "cuisine": "Italian"},
    )
    return response.json()["id"]


def test_add_menu_item_works(tmp_path, monkeypatch):
    menu_items_file = setup_test_files(tmp_path, monkeypatch)
    client = TestClient(app)
    restaurant_id = create_test_restaurant(client)

    response = client.post(
        f"/api/restaurants/{restaurant_id}/menu-items",
        json={"name": "Margherita", "description": "Classic pizza", "price": "12.50"},
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
        "/api/restaurants/fake-id/menu-items",
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
        f"/api/restaurants/{restaurant_id}/menu-items",
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
        f"/api/restaurants/{restaurant_id}/menu-items",
        json={"name": "Margherita", "price": -5},
    )

    assert response.status_code == 422

    saved_items = json.loads(menu_items_file.read_text())
    assert len(saved_items) == 0

def create_test_menu_item(client, restaurant_id):
    response = client.post(
        f"/api/restaurants/{restaurant_id}/menu-items",
        json={"name": "Margherita", "description": "Classic pizza", "price": 12.5},
    )
    return response.json()
 
def test_update_menu_item_only_changes_that_item(tmp_path, monkeypatch):
    menu_items_file = setup_test_files(tmp_path, monkeypatch)
    client = TestClient(app)
    restaurant_id = create_test_restaurant(client)
    first = create_test_menu_item(client, restaurant_id)
    second = create_test_menu_item(client, restaurant_id)

    client.patch(
        f"/api/restaurants/{restaurant_id}/menu-items/{first['id']}",
        json={"price": 20.0},
    )
    saved_item = json.loads(menu_items_file.read_text())
    by_id = {i["id"]:i for i in saved_item}
    assert by_id[first["id"]]["price"] == 20.0
    assert by_id[second["id"]]["price"] == 12.5

def test_update_unknown_menu_item_gives_404(tmp_path, monkeypatch):
    menu_items_file = setup_test_files(tmp_path, monkeypatch)
    client = TestClient(app)
    restaurant_id = create_test_restaurant(client)
 
    response = client.patch(
        f"/api/restaurants/{restaurant_id}/menu-items/fake-item",
        json={"price": 15.0},
    )
 
    assert response.status_code == 404
 
    saved_items = json.loads(menu_items_file.read_text())
    assert len(saved_items) == 0

def test_update_menu_item_with_negative_price_gives_422(tmp_path, monkeypatch):
    menu_items_file = setup_test_files(tmp_path, monkeypatch)
    client = TestClient(app)
    restaurant_id = create_test_restaurant(client)
    item = create_test_menu_item(client, restaurant_id)
 
    response = client.patch(
        f"/api/restaurants/{restaurant_id}/menu-items/{item['id']}",
        json={"price": -5},
    )
 
    assert response.status_code == 422
 
    saved_items = json.loads(menu_items_file.read_text())
    assert saved_items[0]["price"] == 12.5
  