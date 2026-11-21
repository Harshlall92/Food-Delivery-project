import pytest

from app.schemas.cart import CartItemAdd
from app.schemas.menu_item import MenuItem
from app.schemas.restaurant import Restaurant
from app.services import carts_service
from app.services.exceptions import *
from tests.util.builders import create_test_cart, create_test_cart_item
from tests.util.fixtures import anyio_backend, cart_repository, restaurant_repository, menu_item_repository
from app.services.carts_service import *
from tests.util.fixtures import cart_repository
from tests.util.builders import create_test_cart

class TestDeleteCart:

    @pytest.mark.anyio
    async def test_delete_cart_success(self, cart_repository):
        await cart_repository.add_record(create_test_cart(customer_id="test_user_id"))

        assert await delete_cart(cart_repository, "test_user_id")

@pytest.mark.anyio
async def test_retrieve_cart_not_found(cart_repository, restaurant_repository, menu_item_repository):
    with pytest.raises(CartNotFoundError):
        await carts_service.retrieve_cart(cart_repository, restaurant_repository, menu_item_repository, "nobody")

async def seed_add_item_data(cart_repository, restaurant_repository, menu_item_repository):
    """One restaurant with an active, an inactive, and another restaurant's menu item,
    plus a cart for customer c1 containing 1 x m1."""
    restaurant = Restaurant(id="r1", name="Kin&Folk", address="1 Main", cuisine="korean")
    other_restaurant = Restaurant(id="r2", name="Other Place", address="2 Main", cuisine="italian")
    await restaurant_repository.add_record(restaurant)
    await restaurant_repository.add_record(other_restaurant)

    await menu_item_repository.add_record(MenuItem(id="m1", restaurant_id="r1", name="Pizza", price=5.0))
    await menu_item_repository.add_record(MenuItem(id="m2", restaurant_id="r1", name="Soda", price=2.5))
    await menu_item_repository.add_record(MenuItem(id="m3", restaurant_id="r1", name="Soup", price=4.0, available=False))
    await menu_item_repository.add_record(MenuItem(id="m4", restaurant_id="r2", name="Pasta", price=12.0))

    await cart_repository.add_record(create_test_cart(
        customer_id="c1",
        restaurant_id="r1",
        items=[create_test_cart_item(menu_item_id="m1", quantity=1, price="5.00")],
        subtotal="5.00",
    ))


class TestAddItemToCart:

    @pytest.mark.anyio
    async def test_add_new_item_is_added_and_persisted(self, cart_repository, restaurant_repository, menu_item_repository):
        await seed_add_item_data(cart_repository, restaurant_repository, menu_item_repository)

        result = await carts_service.add_item_to_cart(
            cart_repository, menu_item_repository, "c1", CartItemAdd(menu_item_id="m2", quantity=2)
        )

        assert [(i.menu_item_id, i.quantity) for i in result.items] == [("m1", 1), ("m2", 2)]
        assert result.items[1].price == Decimal("2.50")
        assert result.subtotal == Decimal("10.00")

        saved = await cart_repository.get_cart_by_customer_id("c1")
        assert saved == result

    @pytest.mark.anyio
    async def test_add_existing_item_increases_quantity(self, cart_repository, restaurant_repository, menu_item_repository):
        await seed_add_item_data(cart_repository, restaurant_repository, menu_item_repository)

        result = await carts_service.add_item_to_cart(
            cart_repository, menu_item_repository, "c1", CartItemAdd(menu_item_id="m1", quantity=3)
        )

        assert len(result.items) == 1
        assert result.items[0].quantity == 4
        assert result.subtotal == Decimal("20.00")

        saved = await cart_repository.get_cart_by_customer_id("c1")
        assert saved.items[0].quantity == 4

    @pytest.mark.anyio
    async def test_add_item_cart_not_found(self, cart_repository, restaurant_repository, menu_item_repository):
        await seed_add_item_data(cart_repository, restaurant_repository, menu_item_repository)

        with pytest.raises(CartNotFoundError, match="No active cart found for customer nobody."):
            await carts_service.add_item_to_cart(
                cart_repository, menu_item_repository, "nobody", CartItemAdd(menu_item_id="m2")
            )

    @pytest.mark.anyio
    async def test_add_item_menu_item_not_found(self, cart_repository, restaurant_repository, menu_item_repository):
        await seed_add_item_data(cart_repository, restaurant_repository, menu_item_repository)

        with pytest.raises(MenuItemNotFoundError, match="Menu item with id missing not found."):
            await carts_service.add_item_to_cart(
                cart_repository, menu_item_repository, "c1", CartItemAdd(menu_item_id="missing")
            )

    @pytest.mark.anyio
    async def test_add_inactive_menu_item_raises(self, cart_repository, restaurant_repository, menu_item_repository):
        await seed_add_item_data(cart_repository, restaurant_repository, menu_item_repository)

        with pytest.raises(InactiveMenuItemError, match="Menu item with id m3 is not available."):
            await carts_service.add_item_to_cart(
                cart_repository, menu_item_repository, "c1", CartItemAdd(menu_item_id="m3")
            )

        saved = await cart_repository.get_cart_by_customer_id("c1")
        assert len(saved.items) == 1

    @pytest.mark.anyio
    async def test_add_item_from_different_restaurant_raises(self, cart_repository, restaurant_repository, menu_item_repository):
        await seed_add_item_data(cart_repository, restaurant_repository, menu_item_repository)

        with pytest.raises(InvalidMenuItemError):
            await carts_service.add_item_to_cart(
                cart_repository, menu_item_repository, "c1", CartItemAdd(menu_item_id="m4")
            )

        saved = await cart_repository.get_cart_by_customer_id("c1")
        assert len(saved.items) == 1
    @pytest.mark.anyio
    async def test_delete_cart_not_found(self, cart_repository):
        assert not await delete_cart(cart_repository, "non_existent_user_id")


        
