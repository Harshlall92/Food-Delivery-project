from decimal import Decimal

import pytest

from app.schemas.menu_item import MenuItem
from app.schemas.order import OrderCreate, OrderStatusUpdate
from app.schemas.restaurant import Restaurant
from app.services import order_service
from app.services.exceptions import (
    CartNotFoundError,
    CartRestaurantMismatchError,
    CustomerNotFoundError,
    EmptyCartCheckoutError,
    InactiveMenuItemError,
    InactiveRestaurantError,
    InactiveUserError,
    InvalidRoleError,
    MenuItemNotFoundError,
    RestaurantNotFoundError,
    InvalidOrderStatusError,
    OrderNotFoundError
)
from tests.util.builders import create_test_cart, create_test_cart_item, create_test_order, create_test_order_item
from tests.util.fixtures import (
    cart_repository, menu_item_repository, order_item_repository,
    order_repository, restaurant_repository, user_repository,
)
from tests.util.helpers import create_test_customer, create_test_restaurant_owner


@pytest.fixture
def repositories(order_repository, order_item_repository, cart_repository,
                 user_repository, restaurant_repository, menu_item_repository):
    return (order_repository, order_item_repository, cart_repository,
            user_repository, restaurant_repository, menu_item_repository)


async def seed_checkout_data(repositories):
    """Customers (active, inactive, owner), an active and an inactive restaurant, and menu items:
    m1 and m2 available in r1, m3 unavailable in r1, m4 available in r2."""
    _, _, _, user_repository, restaurant_repository, menu_item_repository = repositories

    customer = create_test_customer(email="customer@example.com")
    inactive_customer = create_test_customer(email="inactive@example.com").model_copy(update={"active": False})
    owner = create_test_restaurant_owner(email="owner@example.com")
    for user in (customer, inactive_customer, owner):
        await user_repository.add_record(user)

    await restaurant_repository.add_record(Restaurant(id="r1", name="Open", address="1 Main", cuisine="korean"))
    await restaurant_repository.add_record(Restaurant(id="r2", name="Closed", address="2 Main", cuisine="thai", active=False))

    await menu_item_repository.add_record(MenuItem(id="m1", restaurant_id="r1", name="Pizza", price=5.0))
    await menu_item_repository.add_record(MenuItem(id="m2", restaurant_id="r1", name="Soda", price=2.5))
    await menu_item_repository.add_record(MenuItem(id="m3", restaurant_id="r1", name="Soup", price=4.0, available=False))
    await menu_item_repository.add_record(MenuItem(id="m4", restaurant_id="r2", name="Curry", price=9.0))

    return customer, inactive_customer, owner


async def add_cart(repositories, customer_id, restaurant_id="r1", items=None):
    cart_repository = repositories[2]
    if items is None:
        items = [create_test_cart_item(menu_item_id="m1", quantity=2, price="4.00")]
    await cart_repository.add_record(create_test_cart(customer_id=customer_id, restaurant_id=restaurant_id, items=items))


async def checkout(repositories, customer_id):
    return await order_service.checkout_cart(*repositories, OrderCreate(customer_id=customer_id))


class TestCheckoutSuccess:

    @pytest.mark.anyio
    async def test_checkout_persists_order_and_items_and_deletes_cart(self, repositories):
        order_repository, order_item_repository, cart_repository, *_ = repositories
        customer, _, _ = await seed_checkout_data(repositories)
        await add_cart(repositories, customer.id, items=[
            create_test_cart_item(menu_item_id="m1", quantity=2, price="4.00"),
            create_test_cart_item(menu_item_id="m2", quantity=1, price="2.50"),
        ])

        order = await checkout(repositories, customer.id)

        assert order.customer_id == customer.id
        assert order.restaurant_id == "r1"
        assert order.status == "pending"
        assert await order_repository.get_by_id(order.id) == order

        items = await order_item_repository.get_items_by_order_id(order.id)
        assert [(i.menu_item_id, i.quantity, i.price_per_item) for i in items] == [
            ("m1", 2, Decimal("5.00")),
            ("m2", 1, Decimal("2.50")),
        ]

        assert await cart_repository.get_cart_by_customer_id(customer.id) is None

    @pytest.mark.anyio
    async def test_checkout_recalculates_total_from_current_prices(self, repositories):
        customer, _, _ = await seed_checkout_data(repositories)
        # The cart stored pizza at 4.00, but the menu now says 5.00
        await add_cart(repositories, customer.id)

        order = await checkout(repositories, customer.id)

        assert order.total == Decimal("10.00")


class TestCheckoutCustomerErrors:

    @pytest.mark.anyio
    async def test_customer_not_found(self, repositories):
        await seed_checkout_data(repositories)

        with pytest.raises(CustomerNotFoundError):
            await checkout(repositories, "missing")

    @pytest.mark.anyio
    async def test_user_is_not_a_customer(self, repositories):
        _, _, owner = await seed_checkout_data(repositories)

        with pytest.raises(InvalidRoleError):
            await checkout(repositories, owner.id)

    @pytest.mark.anyio
    async def test_customer_is_inactive(self, repositories):
        _, inactive_customer, _ = await seed_checkout_data(repositories)

        with pytest.raises(InactiveUserError):
            await checkout(repositories, inactive_customer.id)


class TestCheckoutCartErrors:

    @pytest.mark.anyio
    async def test_cart_not_found(self, repositories):
        customer, _, _ = await seed_checkout_data(repositories)

        with pytest.raises(CartNotFoundError):
            await checkout(repositories, customer.id)

    @pytest.mark.anyio
    async def test_empty_cart(self, repositories):
        order_repository = repositories[0]
        customer, _, _ = await seed_checkout_data(repositories)
        await add_cart(repositories, customer.id, items=[])

        with pytest.raises(EmptyCartCheckoutError):
            await checkout(repositories, customer.id)
        assert await order_repository.get_all() == []


class TestCheckoutRestaurantErrors:

    @pytest.mark.anyio
    async def test_restaurant_not_found(self, repositories):
        customer, _, _ = await seed_checkout_data(repositories)
        await add_cart(repositories, customer.id, restaurant_id="missing")

        with pytest.raises(RestaurantNotFoundError):
            await checkout(repositories, customer.id)

    @pytest.mark.anyio
    async def test_restaurant_inactive(self, repositories):
        customer, _, _ = await seed_checkout_data(repositories)
        await add_cart(repositories, customer.id, restaurant_id="r2",
                       items=[create_test_cart_item(menu_item_id="m4", price="9.00")])

        with pytest.raises(InactiveRestaurantError):
            await checkout(repositories, customer.id)


class TestCheckoutMenuItemErrors:

    @pytest.mark.anyio
    async def test_menu_item_not_found(self, repositories):
        customer, _, _ = await seed_checkout_data(repositories)
        await add_cart(repositories, customer.id, items=[create_test_cart_item(menu_item_id="missing")])

        with pytest.raises(MenuItemNotFoundError):
            await checkout(repositories, customer.id)

    @pytest.mark.anyio
    async def test_menu_item_inactive(self, repositories):
        order_repository, _, cart_repository, *_ = repositories
        customer, _, _ = await seed_checkout_data(repositories)
        await add_cart(repositories, customer.id, items=[create_test_cart_item(menu_item_id="m3")])

        with pytest.raises(InactiveMenuItemError):
            await checkout(repositories, customer.id)
        # A failed checkout saves nothing and keeps the cart
        assert await order_repository.get_all() == []
        assert await cart_repository.get_cart_by_customer_id(customer.id) is not None

    @pytest.mark.anyio
    async def test_menu_item_from_another_restaurant(self, repositories):
        customer, _, _ = await seed_checkout_data(repositories)
        await add_cart(repositories, customer.id, items=[create_test_cart_item(menu_item_id="m4")])

        with pytest.raises(CartRestaurantMismatchError):
            await checkout(repositories, customer.id)

ALLOWED_STATUSES = ["pending", "confirmed", "preparing", "ready", "picked up", "delivered", "cancelled"]


class TestUpdateOrderStatus:

    @pytest.mark.anyio
    async def test_update_status_returns_updated_order(self, order_repository):
        order = create_test_order()
        await order_repository.add_record(order)

        result = await order_service.update_order_status(order_repository, order.id, OrderStatusUpdate(status="confirmed"))

        assert result.status == "confirmed"
        assert result.id == order.id
        assert result.total == order.total
        assert result.customer_id == order.customer_id

    @pytest.mark.anyio
    async def test_update_status_is_persisted(self, order_repository):
        order = create_test_order()
        await order_repository.add_record(order)

        await order_service.update_order_status(order_repository, order.id, OrderStatusUpdate(status="ready"))

        assert (await order_repository.get_by_id(order.id)).status == "ready"

    @pytest.mark.anyio
    @pytest.mark.parametrize("new_status", ALLOWED_STATUSES)
    async def test_every_allowed_status(self, order_repository, new_status):
        order = create_test_order()
        await order_repository.add_record(order)

        result = await order_service.update_order_status(order_repository, order.id, OrderStatusUpdate(status=new_status))

        assert result.status == new_status

    @pytest.mark.anyio
    @pytest.mark.parametrize("bad_status", ["shipped", "Pending", "picked_up", ""])
    async def test_invalid_status_is_rejected(self, order_repository, bad_status):
        order = create_test_order()
        await order_repository.add_record(order)

        # model_construct skips Pydantic validation, so the service's own check is what's tested
        with pytest.raises(InvalidOrderStatusError):
            await order_service.update_order_status(
                order_repository, order.id, OrderStatusUpdate.model_construct(status=bad_status)
            )
        assert (await order_repository.get_by_id(order.id)).status == "pending"

    @pytest.mark.anyio
    async def test_missing_order_raises(self, order_repository):
        with pytest.raises(OrderNotFoundError, match="Order with id missing not found."):
            await order_service.update_order_status(order_repository, "missing", OrderStatusUpdate(status="ready"))

async def seed_orders(repositories):
    """Three orders on top of the checkout data: two for the customer (r1 pending, r2 ready)
    and one for the second customer (r1 ready), each with one item."""
    order_repository, order_item_repository, *_ = repositories
    customer, other_customer, _ = await seed_checkout_data(repositories)

    orders = [
        create_test_order(customer_id=customer.id, restaurant_id="r1", status="pending", total="10.00"),
        create_test_order(customer_id=customer.id, restaurant_id="r2", status="ready", total="9.00"),
        create_test_order(customer_id=other_customer.id, restaurant_id="r1", status="ready", total="2.50"),
    ]
    for order, (menu_item_id, quantity, price) in zip(orders, [("m1", 2, "5.00"), ("m4", 1, "9.00"), ("m2", 1, "2.50")]):
        await order_repository.add_record(order)
        await order_item_repository.add_order_items([
            create_test_order_item(order_id=order.id, menu_item_id=menu_item_id, quantity=quantity, price_per_item=price)
        ])

    return customer, other_customer, orders


async def get_order(repositories, order_id):
    order_repository, order_item_repository, _, user_repository, restaurant_repository, menu_item_repository = repositories
    return await order_service.get_order(
        order_repository, order_item_repository, user_repository, restaurant_repository, menu_item_repository, order_id
    )


async def query_orders(repositories, **filters):
    order_repository, order_item_repository, _, user_repository, restaurant_repository, menu_item_repository = repositories
    return await order_service.query_orders(
        order_repository, order_item_repository, user_repository, restaurant_repository, menu_item_repository, **filters
    )


class TestGetOrder:

    @pytest.mark.anyio
    async def test_get_order_returns_response_with_items(self, repositories):
        _, _, orders = await seed_orders(repositories)

        response = await get_order(repositories, orders[0].id)

        assert response.order_id == orders[0].id
        assert response.customer_name == "Test User"
        assert response.restaurant_name == "Open"
        assert response.status == "pending"
        assert response.total == Decimal("10.00")
        assert [(i.menu_item_name, i.quantity, i.price_per_item) for i in response.items] == [
            ("Pizza", 2, Decimal("5.00"))
        ]

    @pytest.mark.anyio
    async def test_get_order_missing_raises(self, repositories):
        with pytest.raises(OrderNotFoundError, match="Order with id missing not found."):
            await get_order(repositories, "missing")


class TestQueryOrders:

    @pytest.mark.anyio
    async def test_no_filters_returns_all_orders_with_items(self, repositories):
        _, _, orders = await seed_orders(repositories)

        responses = await query_orders(repositories)

        assert [r.order_id for r in responses] == [o.id for o in orders]
        assert all(len(r.items) == 1 for r in responses)

    @pytest.mark.anyio
    async def test_filter_by_customer(self, repositories):
        customer, _, orders = await seed_orders(repositories)

        responses = await query_orders(repositories, customer_id=customer.id)

        assert [r.order_id for r in responses] == [orders[0].id, orders[1].id]

    @pytest.mark.anyio
    async def test_filter_by_restaurant(self, repositories):
        _, _, orders = await seed_orders(repositories)

        responses = await query_orders(repositories, restaurant_id="r1")

        assert [r.order_id for r in responses] == [orders[0].id, orders[2].id]

    @pytest.mark.anyio
    async def test_filter_by_status(self, repositories):
        _, _, orders = await seed_orders(repositories)

        responses = await query_orders(repositories, status="ready")

        assert [r.order_id for r in responses] == [orders[1].id, orders[2].id]

    @pytest.mark.anyio
    async def test_combined_filters(self, repositories):
        customer, _, orders = await seed_orders(repositories)

        responses = await query_orders(repositories, customer_id=customer.id, status="ready")

        assert [r.order_id for r in responses] == [orders[1].id]
        assert responses[0].restaurant_name == "Closed"

    @pytest.mark.anyio
    async def test_no_matching_orders_returns_empty_list(self, repositories):
        await seed_orders(repositories)

        assert await query_orders(repositories, customer_id="nobody") == []