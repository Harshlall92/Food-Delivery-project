from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.schemas.restaurant import Restaurant
from app.services import menu_item_service as mService


client = TestClient(app)


TEST_RESTAURANT = Restaurant(
    id="01a0fd78-2c5c-72f4-b913-672a802a7116",
    name="kin&folk kelowna",
    address="281 lawrence avenue",
    cuisine="korean",
)


def test_search_success():
    with patch(
        "app.api.routes.restaurants.rService.get_restaurants_by_name",
        new_callable=AsyncMock,
        return_value=[TEST_RESTAURANT],
    ):
        response = client.get("/api/restaurants/search", params={"name": "kin"})

    assert response.status_code == 200
    assert response.json()[0]["name"] == "kin&folk kelowna"


def test_search_not_found():
    with patch(
        "app.api.routes.restaurants.rService.get_restaurants_by_name",
        new_callable=AsyncMock,
        side_effect=mService.RestaurantNotFoundError("No restaurants found matching zzz."),
    ):
        response = client.get("/api/restaurants/search", params={"name": "zzz"})

    assert response.status_code == 404


def test_filter_success():
    with patch(
        "app.api.routes.restaurants.rService.get_restaurants_by_cuisine",
        new_callable=AsyncMock,
        return_value=[TEST_RESTAURANT],
    ):
        response = client.get("/api/restaurants/filter", params={"cuisine": "korean"})

    assert response.status_code == 200
    assert response.json()[0]["cuisine"] == "korean"


def test_filter_not_found():
    with patch(
        "app.api.routes.restaurants.rService.get_restaurants_by_cuisine",
        new_callable=AsyncMock,
        side_effect=mService.RestaurantNotFoundError("Restaurant with cuisine mexican not found."),
    ):
        response = client.get("/api/restaurants/filter", params={"cuisine": "mexican"})

    assert response.status_code == 404