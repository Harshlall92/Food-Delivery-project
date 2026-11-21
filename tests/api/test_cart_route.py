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

def test_get_cart_invalid_id_returns_422(tmp_path, monkeypatch):
    setup_files(tmp_path, monkeypatch, carts=[], restaurants=[], menu_items=[])
    response = TestClient(app).get("/api/carts/not-a-uuid")
    assert response.status_code == 422