from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.restaurant import Restaurant

client = TestClient(app)

def test_get_restaurant():
    fake_data = [
        Restaurant(
            id = 1,
            name = "place",
            address = "street",
            category = "type"
            ),
    ]
    with patch(
        "app.api.routes.restaurants.rService.get_restaurants",
        new_callable=AsyncMock,
        return_value = fake_data
    ):
        response = client.get("/restaurants")
    assert response.status_code == 200
    assert response.json() == [
        {"id" : 1, "name" : "place", "address" : "street", "category" : "type"}
    ]

def test_get_restaurant_fail():
    client = TestClient(app, raise_server_exceptions = False)
    with patch(
        "app.api.routes.restaurants.rService.get_restaurants",
        new_callable=AsyncMock,
        side_effect = ValueError(),
    ):
        response = client.get("/restaurants")
    assert response.status_code == 500