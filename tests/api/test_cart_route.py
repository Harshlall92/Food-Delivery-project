import json
from fastapi.testclient import TestClient
from app.main import app

CUSTOMER_ID = "01a1e9a4-021a-7f27-8546-c524b7f1ae7b"
MISSING_ID = "00000000-0000-0000-0000-000000000000"


def setup_files(tmp_path, monkeypatch, carts, restaurants, menu_items):
    for name, module, data in [
        ("carts.json", "cart_repository", carts),
        ("restaurants.json", "restaurant_repository", restaurants),
        ("menu-items.json", "menu_item_repository", menu_items),
    ]:
        f = tmp_path / name
        f.write_text(json.dumps(data))
        monkeypatch.setattr(f"app.repositories.{module}.FILE_PATH", str(f))

def test_get_cart_returns_200(tmp_path, monkeypatch):
    setup_files(
        tmp_path, monkeypatch,
        carts=[{"id": CUSTOMER_ID, "restaurant_id": "r1",
                "items": [{"menu_item_id": "m1", "quantity": 2, "price": "4.00"}],
                "subtotal": "8.00"}],
        restaurants=[{"id": "r1", "name": "Testaurant", "address": "a", "cuisine": "c", "active": True}],
        menu_items=[{"id": "m1", "restaurant_id": "r1", "name": "Taco", "price": 4.0,
                     "description": "", "available": True}],
    )
    response = TestClient(app).get(f"/api/carts/{CUSTOMER_ID}")

    assert response.status_code == 200
    body = response.json()
    assert body["restaurant_name"] == "Testaurant"
    assert body["items"][0]["menu_item_name"] == "Taco"
    assert body["total_quantity"] == 2
    assert body["sub_total"] == "8.00"

def test_get_cart_returns_404(tmp_path, monkeypatch):
    setup_files(tmp_path, monkeypatch, carts=[], restaurants=[], menu_items=[])
    response = TestClient(app).get(f"/api/carts/{MISSING_ID}")
    assert response.status_code == 404

def setup_add_item_files(tmp_path, monkeypatch):
    setup_files(
        tmp_path, monkeypatch,
        carts=[{"id": CUSTOMER_ID, "restaurant_id": "r1",
                "items": [{"menu_item_id": "m1", "quantity": 1, "price": "4.00"}],
                "subtotal": "4.00"}],
        restaurants=[
            {"id": "r1", "name": "Testaurant", "address": "a", "cuisine": "c", "active": True},
            {"id": "r2", "name": "Elsewhere", "address": "b", "cuisine": "d", "active": True},
        ],
        menu_items=[
            {"id": "m1", "restaurant_id": "r1", "name": "Taco", "price": 4.0, "description": "", "available": True},
            {"id": "m2", "restaurant_id": "r1", "name": "Nachos", "price": 6.0, "description": "", "available": True},
            {"id": "m3", "restaurant_id": "r1", "name": "Churro", "price": 3.0, "description": "", "available": False},
            {"id": "m4", "restaurant_id": "r2", "name": "Pasta", "price": 12.0, "description": "", "available": True},
        ],
    )


def test_add_item_full_workflow(tmp_path, monkeypatch):
    setup_add_item_files(tmp_path, monkeypatch)
    client = TestClient(app)

    response = client.post(f"/api/carts/{CUSTOMER_ID}/items", json={"menu_item_id": "m2", "quantity": 2})
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == CUSTOMER_ID
    assert [(i["menu_item_id"], i["quantity"]) for i in body["items"]] == [("m1", 1), ("m2", 2)]
    assert body["subtotal"] == "16.00"

    response = client.post(f"/api/carts/{CUSTOMER_ID}/items", json={"menu_item_id": "m1", "quantity": 3})
    assert response.status_code == 200
    assert response.json()["items"][0]["quantity"] == 4

    # The changes are saved: retrieving the cart shows both items
    cart = client.get(f"/api/carts/{CUSTOMER_ID}").json()
    assert [i["menu_item_name"] for i in cart["items"]] == ["Taco", "Nachos"]
    assert cart["total_quantity"] == 6
    assert cart["sub_total"] == "28.00"


def test_add_item_invalid_body_returns_422(tmp_path, monkeypatch):
    setup_add_item_files(tmp_path, monkeypatch)
    client = TestClient(app)

    assert client.post(f"/api/carts/{CUSTOMER_ID}/items", json={"menu_item_id": "m2", "quantity": 0}).status_code == 422
    assert client.post(f"/api/carts/{CUSTOMER_ID}/items", json={"menu_item_id": "m2", "quantity": -1}).status_code == 422
    assert client.post(f"/api/carts/{CUSTOMER_ID}/items", json={"quantity": 1}).status_code == 422


def test_add_item_cart_not_found_returns_404(tmp_path, monkeypatch):
    setup_add_item_files(tmp_path, monkeypatch)
    response = TestClient(app).post(f"/api/carts/{MISSING_ID}/items", json={"menu_item_id": "m2"})
    assert response.status_code == 404


def test_add_item_menu_item_not_found_returns_404(tmp_path, monkeypatch):
    setup_add_item_files(tmp_path, monkeypatch)
    response = TestClient(app).post(f"/api/carts/{CUSTOMER_ID}/items", json={"menu_item_id": "missing"})
    assert response.status_code == 404


def test_add_item_inactive_menu_item_returns_422(tmp_path, monkeypatch):
    setup_add_item_files(tmp_path, monkeypatch)
    response = TestClient(app).post(f"/api/carts/{CUSTOMER_ID}/items", json={"menu_item_id": "m3"})
    assert response.status_code == 422
    assert "not available" in response.json()["detail"]


def test_add_item_from_different_restaurant_returns_422(tmp_path, monkeypatch):
    setup_add_item_files(tmp_path, monkeypatch)
    response = TestClient(app).post(f"/api/carts/{CUSTOMER_ID}/items", json={"menu_item_id": "m4"})
    assert response.status_code == 422
    assert "same restaurant" in response.json()["detail"]