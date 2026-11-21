from decimal import Decimal

import pytest

from app.schemas.cart import CartItemAdd
from app.schemas.menu_item import MenuItem
from app.schemas.restaurant import Restaurant
from app.services import carts_service
from app.services.exceptions import (
    CartNotFoundError,
    CustomerNotFoundError,
    DuplicateCartError,
    InactiveMenuItemError,
    InactiveUserError,
    InvalidMenuItemError,
    InvalidRoleError,
    MenuItemNotFoundError,
)
from tests.util.builders import create_test_cart, create_test_cart_item, create_test_cart_create
from tests.util.fixtures import anyio_backend, cart_repository, menu_item_repository, restaurant_repository, user_repository
from tests.util.helpers import create_test_customer, create_test_restaurant_owner

class TestRetrieveCart:

    @pytest.mark.anyio
    async def test_retrieve_cart_builds_response(self, cart_repository, restaurant_repository, menu_item_repository):
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
    async def test_retrieve_cart_not_found(self, cart_repository, restaurant_repository, menu_item_repository):
        with pytest.raises(CartNotFoundError):
            await carts_service.retrieve_cart(cart_repository, restaurant_repository, menu_item_repository, "nobody")


async def seed_add_item_data(cart_repository, restaurant_repository, menu_item_repository):
    """One restaurant with an active, an inactive, and another restaurant's menu item,
    plus a cart for customer c1 containing 1 x m1."""
    await restaurant_repository.add_record(Restaurant(id="r1", name="Kin&Folk", address="1 Main", cuisine="korean"))
    await restaurant_repository.add_record(Restaurant(id="r2", name="Other Place", address="2 Main", cuisine="italian"))

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
        assert await cart_repository.get_cart_by_customer_id("c1") == result

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


class TestDeleteCart:

    @pytest.mark.anyio
    async def test_delete_cart_removes_cart_from_file(self, cart_repository):
        await cart_repository.add_record(create_test_cart(customer_id="test_user_id"))
        await cart_repository.add_record(create_test_cart(customer_id="other_user_id"))

        assert await carts_service.delete_cart(cart_repository, "test_user_id") is True

        assert await cart_repository.get_cart_by_customer_id("test_user_id") is None
        remaining = await cart_repository.get_all()
        assert [c.customer_id for c in remaining] == ["other_user_id"]

    @pytest.mark.anyio
    async def test_delete_cart_not_found_raises(self, cart_repository):
        with pytest.raises(CartNotFoundError, match="Cart for customer with id non_existent_user_id not found."):
            await carts_service.delete_cart(cart_repository, "non_existent_user_id")



@pytest.fixture
async def setup(cart_repository, user_repository, menu_item_repository, restaurant_repository):
    customer = create_test_customer()
    await user_repository.add_record(customer)

    restaurant = Restaurant(name="Test Restaurant", address="1 Main St", cuisine="thai")
    await restaurant_repository.add_record(restaurant)

    menu_item = MenuItem(restaurant_id=restaurant.id, name="Pad Thai", price=12.5)
    await menu_item_repository.add_record(menu_item)

    return {
        "cart_repo": cart_repository,
        "user_repo": user_repository,
        "menu_repo": menu_item_repository,
        "restaurant_repo": restaurant_repository,
        "customer": customer,
        "restaurant": restaurant,
        "menu_item": menu_item,
    }


async def make_cart(setup, customer_id, menu_item_id, quantity=1):
    data = create_test_cart_create(customer_id=customer_id, menu_item_id=menu_item_id, quantity=quantity)
    return await carts_service.create_cart(setup["cart_repo"], setup["user_repo"], setup["menu_repo"], setup["restaurant_repo"], data)


class TestCreateCart:

    @pytest.mark.anyio
    async def test_create_cart_success(self, setup):
        cart = await make_cart(setup, setup["customer"].id, setup["menu_item"].id, quantity=2)

        assert cart.subtotal == Decimal("25.00")
        assert await setup["cart_repo"].get_by_id(setup["customer"].id) is not None

    @pytest.mark.anyio
    async def test_customer_not_found(self, setup):
        with pytest.raises(CustomerNotFoundError):
            await make_cart(setup, "missing", setup["menu_item"].id)

        assert await setup["cart_repo"].get_all() == []

    @pytest.mark.anyio
    async def test_user_is_not_a_customer(self, setup):
        owner = create_test_restaurant_owner(email="owner@example.com")
        await setup["user_repo"].add_record(owner)

        with pytest.raises(InvalidRoleError):
            await make_cart(setup, owner.id, setup["menu_item"].id)

    @pytest.mark.anyio
    async def test_customer_is_inactive(self, setup):
        inactive = create_test_customer(email="inactive@example.com")
        inactive.active = False
        await setup["user_repo"].add_record(inactive)

        with pytest.raises(InactiveUserError):
            await make_cart(setup, inactive.id, setup["menu_item"].id)

    @pytest.mark.anyio
    async def test_customer_already_has_cart(self, setup):
        await setup["cart_repo"].add_record(create_test_cart(customer_id=setup["customer"].id))

        with pytest.raises(DuplicateCartError):
            await make_cart(setup, setup["customer"].id, setup["menu_item"].id)

    @pytest.mark.anyio
    async def test_menu_item_not_found(self, setup):
        with pytest.raises(MenuItemNotFoundError):
            await make_cart(setup, setup["customer"].id, "missing")

        assert await setup["cart_repo"].get_all() == []

    @pytest.mark.anyio
    async def test_menu_item_unavailable(self, setup):
        item = MenuItem(restaurant_id=setup["restaurant"].id, name="Green Curry", price=14.0, available=False)
        await setup["menu_repo"].add_record(item)

        with pytest.raises(InactiveMenuItemError):
            await make_cart(setup, setup["customer"].id, item.id)

        assert await setup["cart_repo"].get_all() == []

    @pytest.mark.anyio
    async def test_restaurant_is_inactive(self, setup):
        
        closed = Restaurant(name="Closed", address="2 Main St", cuisine="thai", active=False)
        await setup["restaurant_repo"].add_record(closed)
        item = MenuItem(restaurant_id=closed.id, name="Soup", price=5.0)
        await setup["menu_repo"].add_record(item)

        with pytest.raises(InactiveMenuItemError):
            await make_cart(setup, setup["customer"].id, item.id)

        assert await setup["cart_repo"].get_all() == []