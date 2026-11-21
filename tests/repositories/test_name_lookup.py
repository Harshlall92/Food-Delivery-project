import pytest

from app.repositories.exceptions import MenuItemNotFoundError, RestaurantNotFoundError
from app.schemas.menu_item import MenuItem
from app.schemas.restaurant import Restaurant
from tests.util.fixtures import anyio_backend, restaurant_repository, menu_item_repository

@pytest.mark.anyio
async def test_get_restaurant_name_by_id(restaurant_repository):
    r = Restaurant(name="Kin&Folk", address="1 Main", cuisine="korean")
    await restaurant_repository.add_record(r)
    assert await restaurant_repository.get_restaurant_name_by_id(r.id) == "Kin&Folk"

@pytest.mark.anyio
async def test_get_restaurant_name_by_id_not_found(restaurant_repository):
    with pytest.raises(RestaurantNotFoundError):
        await restaurant_repository.get_restaurant_name_by_id("missing")

@pytest.mark.anyio
async def test_get_menu_item_name_by_id(menu_item_repository):
    m = MenuItem(restaurant_id="r1", name="Pizza", price=10.0)
    await menu_item_repository.add_record(m)
    assert await menu_item_repository.get_menu_item_name_by_id(m.id) == "Pizza"

@pytest.mark.anyio
async def test_get_menu_item_name_by_id_not_found(menu_item_repository):
    with pytest.raises(MenuItemNotFoundError):
        await menu_item_repository.get_menu_item_name_by_id("missing")

@pytest.mark.anyio
async def test_is_restaurant_active_returns_true(restaurant_repository):
    r = Restaurant(name="Open Place", address="1 Main", cuisine="korean")
    await restaurant_repository.add_record(r)
    assert await restaurant_repository.is_restaurant_active(r.id) is True

@pytest.mark.anyio
async def test_is_restaurant_active_returns_false(restaurant_repository):
    r = Restaurant(name="Closed Place", address="1 Main", cuisine="korean", active=False)
    await restaurant_repository.add_record(r)
    assert await restaurant_repository.is_restaurant_active(r.id) is False

@pytest.mark.anyio
async def test_is_restaurant_active_not_found_raises(restaurant_repository):
    with pytest.raises(RestaurantNotFoundError):
        await restaurant_repository.is_restaurant_active("missing")