import pytest

from app.schemas.restaurant import Restaurant
from tests.util.fixtures import anyio_backend, restaurant_repository


@pytest.mark.anyio
async def test_is_restaurant_active_returns_true(restaurant_repository):
    restaurant = Restaurant(name="Open", address="1 Main St", cuisine="thai", active=True)
    await restaurant_repository.add_record(restaurant)

    result = await restaurant_repository.is_restaurant_active(restaurant.id)

    assert result is True


@pytest.mark.anyio
async def test_is_restaurant_active_returns_false(restaurant_repository):
    restaurant = Restaurant(name="Closed", address="2 Main St", cuisine="thai", active=False)
    await restaurant_repository.add_record(restaurant)

    result = await restaurant_repository.is_restaurant_active(restaurant.id)

    assert result is False


@pytest.mark.anyio
async def test_is_restaurant_active_missing_restaurant(restaurant_repository):
    result = await restaurant_repository.is_restaurant_active("missing")

    assert result is False