from decimal import Decimal
import pytest

from app.schemas.menu_item import MenuItem
from app.schemas.restaurant import Restaurant
from app.services import carts_service
from app.services.exceptions import CartNotFoundError
from tests.util.builders import create_test_cart, create_test_cart_item
from tests.util.fixtures import anyio_backend, cart_repository, restaurant_repository, menu_item_repository

@pytest.mark.anyio
async def test_retrieve_cart_builds_response(cart_repository, restaurant_repository, menu_item_repository):
    r = Restaurant(name="Kin&Folk", address="1 Main", cuisine="korean")
    await restaurant_repository.add_record(r)
    pizza = MenuItem(restaurant_id=r.id, name="Pizza", price=5.0)
    soda = MenuItem(restaurant_id=r.id, name="Soda", price=2.5)
    await menu_item_repository.add_record(pizza)
    await menu_item_repository.add_record(soda)
    await cart_repository.add_record(create_test_cart(
        customer_id="c1",
        restaurant_id=r.id,
        items=[
            create_test_cart_item(menu_item_id=pizza.id, quantity=2, price="5.00"),
            create_test_cart_item(menu_item_id=soda.id, quantity=1, price="2.50"),
        ],
    ))

    result = await carts_service.retrieve_cart(cart_repository, restaurant_repository, menu_item_repository, "c1")

    assert result.restaurant_name == "Kin&Folk"
    assert [i.menu_item_name for i in result.items] == ["Pizza", "Soda"]
    assert result.total_quantity == 3
    assert result.sub_total == Decimal("12.50")

@pytest.mark.anyio
async def test_retrieve_cart_not_found(cart_repository, restaurant_repository, menu_item_repository):
    with pytest.raises(CartNotFoundError):
        await carts_service.retrieve_cart(cart_repository, restaurant_repository, menu_item_repository, "nobody")