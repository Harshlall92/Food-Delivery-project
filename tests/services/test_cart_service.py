from decimal import Decimal

import pytest

from app.schemas.cart import CartCreate, CartItemAdd
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
from tests.util.builders import create_test_cart, create_test_cart_item
from tests.util.fixtures import (
    anyio_backend, cart_repository, menu_item_repository, restaurant_repository, user_repository,
)
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

async def seed_create_cart_data(user_repository, restaurant_repository, menu_item_repository):
    """An active customer, an inactive customer, a restaurant owner; one active and one
    inactive restaurant; an available, an unavailable, and an inactive-restaurant menu item."""
    customer = create_test_customer(email="customer@example.com")
    inactive_customer = create_test_customer(email="inactive@example.com").model_copy(update={"active": False})
    owner = create_test_restaurant_owner(email="owner@example.com")
    for user in (customer, inactive_customer, owner):
        await user_repository.add_record(user)

    await restaurant_repository.add_record(Restaurant(id="r1", name="Open", address="1 Main", cuisine="korean"))
    await restaurant_repository.add_record(Restaurant(id="r2", name="Closed", address="2 Main", cuisine="thai", active=False))

    await menu_item_repository.add_record(MenuItem(id="m1", restaurant_id="r1", name="Pizza", price=5.0))
    await menu_item_repository.add_record(MenuItem(id="m2", restaurant_id="r1", name="Soup", price=4.0, available=False))
    await menu_item_repository.add_record(MenuItem(id="m3", restaurant_id="r2", name="Curry", price=9.0))

    return customer, inactive_customer, owner


class TestCreateCart:

    @pytest.mark.anyio
    async def test_create_cart_full_workflow(self, cart_repository, user_repository, menu_item_repository, restaurant_repository):
        customer, _, _ = await seed_create_cart_data(user_repository, restaurant_repository, menu_item_repository)

        cart = await carts_service.create_cart(
            cart_repository, user_repository, menu_item_repository, restaurant_repository,
            CartCreate(customer_id=customer.id, menu_item_id="m1", quantity=2),
        )

        assert cart.customer_id == customer.id
        assert cart.restaurant_id == "r1"
        assert [(i.menu_item_id, i.quantity, i.price) for i in cart.items] == [("m1", 2, Decimal("5.00"))]
        assert cart.subtotal == Decimal("10.00")
        assert await cart_repository.get_active_cart_by_customer_id(customer.id) == cart

    @pytest.mark.anyio
    async def test_create_cart_customer_not_found(self, cart_repository, user_repository, menu_item_repository, restaurant_repository):
        await seed_create_cart_data(user_repository, restaurant_repository, menu_item_repository)

        with pytest.raises(CustomerNotFoundError, match="Customer with id missing not found."):
            await carts_service.create_cart(
                cart_repository, user_repository, menu_item_repository, restaurant_repository,
                CartCreate(customer_id="missing", menu_item_id="m1"),
            )

    @pytest.mark.anyio
    async def test_create_cart_wrong_role(self, cart_repository, user_repository, menu_item_repository, restaurant_repository):
        _, _, owner = await seed_create_cart_data(user_repository, restaurant_repository, menu_item_repository)

        with pytest.raises(InvalidRoleError):
            await carts_service.create_cart(
                cart_repository, user_repository, menu_item_repository, restaurant_repository,
                CartCreate(customer_id=owner.id, menu_item_id="m1"),
            )

    @pytest.mark.anyio
    async def test_create_cart_inactive_customer(self, cart_repository, user_repository, menu_item_repository, restaurant_repository):
        _, inactive_customer, _ = await seed_create_cart_data(user_repository, restaurant_repository, menu_item_repository)

        with pytest.raises(InactiveUserError):
            await carts_service.create_cart(
                cart_repository, user_repository, menu_item_repository, restaurant_repository,
                CartCreate(customer_id=inactive_customer.id, menu_item_id="m1"),
            )

    @pytest.mark.anyio
    async def test_create_cart_duplicate(self, cart_repository, user_repository, menu_item_repository, restaurant_repository):
        customer, _, _ = await seed_create_cart_data(user_repository, restaurant_repository, menu_item_repository)
        data = CartCreate(customer_id=customer.id, menu_item_id="m1")
        await carts_service.create_cart(cart_repository, user_repository, menu_item_repository, restaurant_repository, data)

        with pytest.raises(DuplicateCartError):
            await carts_service.create_cart(cart_repository, user_repository, menu_item_repository, restaurant_repository, data)

    @pytest.mark.anyio
    async def test_create_cart_menu_item_not_found(self, cart_repository, user_repository, menu_item_repository, restaurant_repository):
        customer, _, _ = await seed_create_cart_data(user_repository, restaurant_repository, menu_item_repository)

        with pytest.raises(MenuItemNotFoundError, match="Menu item with id missing not found."):
            await carts_service.create_cart(
                cart_repository, user_repository, menu_item_repository, restaurant_repository,
                CartCreate(customer_id=customer.id, menu_item_id="missing"),
            )

    @pytest.mark.anyio
    async def test_create_cart_inactive_menu_item(self, cart_repository, user_repository, menu_item_repository, restaurant_repository):
        customer, _, _ = await seed_create_cart_data(user_repository, restaurant_repository, menu_item_repository)

        with pytest.raises(InactiveMenuItemError, match="is not available"):
            await carts_service.create_cart(
                cart_repository, user_repository, menu_item_repository, restaurant_repository,
                CartCreate(customer_id=customer.id, menu_item_id="m2"),
            )
        assert await cart_repository.get_active_cart_by_customer_id(customer.id) is None

    @pytest.mark.anyio
    async def test_create_cart_inactive_restaurant(self, cart_repository, user_repository, menu_item_repository, restaurant_repository):
        customer, _, _ = await seed_create_cart_data(user_repository, restaurant_repository, menu_item_repository)

        with pytest.raises(InactiveMenuItemError, match="restaurant that is not active"):
            await carts_service.create_cart(
                cart_repository, user_repository, menu_item_repository, restaurant_repository,
                CartCreate(customer_id=customer.id, menu_item_id="m3"),
            )