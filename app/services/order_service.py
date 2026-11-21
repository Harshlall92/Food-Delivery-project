from decimal import Decimal

from app.repositories.cart_repository import CartRepository
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.order_item_repository import OrderItemRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.user_repository import UserRepository
from app.schemas.order import Order, OrderCreate, OrderItem, OrderItemResponse, OrderResponse, OrderStatus, OrderStatusUpdate
from typing import get_args
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
from app.repositories.exceptions import MenuItemNotFoundError as RepoMenuItemNotFoundError
from app.repositories.exceptions import RestaurantNotFoundError as RepoRestaurantNotFoundError


async def checkout_cart(
        order_repository: OrderRepository,
        order_item_repository: OrderItemRepository,
        cart_repository: CartRepository,
        user_repository: UserRepository,
        restaurant_repository: RestaurantRepository,
        menu_item_repository: MenuItemRepository,
        data: OrderCreate,
        ) -> Order:

    customer = await user_repository.get_by_id(data.customer_id)
    if customer is None:
        raise CustomerNotFoundError(f"Customer with id {data.customer_id} not found.")

    if customer.role != "customer":
        raise InvalidRoleError(f"User with id {data.customer_id} is not a customer.")

    if not customer.active:
        raise InactiveUserError(f"Customer with id {data.customer_id} is not active.")

    cart = await cart_repository.get_cart_by_customer_id(data.customer_id)
    if cart is None:
        raise CartNotFoundError(f"No active cart found for customer {data.customer_id}.")

    if not cart.items:
        raise EmptyCartCheckoutError(f"Cart for customer {data.customer_id} is empty.")

    restaurant = await restaurant_repository.get_by_id(cart.restaurant_id)
    if restaurant is None:
        raise RestaurantNotFoundError(f"Restaurant with id {cart.restaurant_id} not found.")

    if not restaurant.active:
        raise InactiveRestaurantError(f"Restaurant with id {cart.restaurant_id} is not active.")

    prices = []
    for cart_item in cart.items:
        menu_item = await menu_item_repository.get_by_id(cart_item.menu_item_id)
        if menu_item is None:
            raise MenuItemNotFoundError(f"Menu item with id {cart_item.menu_item_id} not found.")

        if not menu_item.available:
            raise InactiveMenuItemError(f"Menu item with id {cart_item.menu_item_id} is not available.")

        if menu_item.restaurant_id != cart.restaurant_id:
            raise CartRestaurantMismatchError(
                f"Menu item with id {cart_item.menu_item_id} does not belong to the cart's restaurant."
            )

        prices.append(Decimal(str(menu_item.price)).quantize(Decimal("0.01")))

    order = Order(
        customer_id=data.customer_id,
        restaurant_id=cart.restaurant_id,
        status="pending",
        total=sum((price * item.quantity for item, price in zip(cart.items, prices)), Decimal("0.00")),
    )
    order_items = [
        OrderItem(order_id=order.id, menu_item_id=item.menu_item_id, quantity=item.quantity, price_per_item=price)
        for item, price in zip(cart.items, prices)
    ]

    await order_repository.add_record(order)
    await order_item_repository.add_order_items(order_items)

    if not await cart_repository.delete_record(data.customer_id):
        raise CartNotFoundError(f"Cart for customer {data.customer_id} could not be deleted after checkout.")

    return order

async def update_order_status(
        order_repository: OrderRepository,
        order_id: str,
        data: OrderStatusUpdate,
        ) -> Order:

    order = await order_repository.get_by_id(order_id)
    if order is None:
        raise OrderNotFoundError(f"Order with id {order_id} not found.")

    if data.status not in get_args(OrderStatus):
        raise InvalidOrderStatusError(f"Status {data.status} is not a valid order status.")

    return await order_repository.update_record(order_id, order.model_copy(update={"status": data.status}))

async def _build_order_response(
        order: Order,
        order_item_repository: OrderItemRepository,
        user_repository: UserRepository,
        restaurant_repository: RestaurantRepository,
        menu_item_repository: MenuItemRepository,
        ) -> OrderResponse:

    customer = await user_repository.get_by_id(order.customer_id)
    if customer is None:
        raise CustomerNotFoundError(f"Customer with id {order.customer_id} not found.")

    try:
        restaurant_name = await restaurant_repository.get_restaurant_name_by_id(order.restaurant_id)
        items = [
            OrderItemResponse(
                menu_item_name=await menu_item_repository.get_menu_item_name_by_id(item.menu_item_id),
                quantity=item.quantity,
                price_per_item=item.price_per_item,
            )
            for item in await order_item_repository.get_items_by_order_id(order.id)
        ]
    except (RepoRestaurantNotFoundError, RepoMenuItemNotFoundError) as e:
        raise ItemNotFoundError(e.message) from e

    return OrderResponse(
        order_id=order.id,
        customer_name=f"{customer.first_name} {customer.last_name}",
        restaurant_name=restaurant_name,
        order_date=order.order_date,
        status=order.status,
        total=order.total,
        items=items,
    )


async def get_order(
        order_repository: OrderRepository,
        order_item_repository: OrderItemRepository,
        user_repository: UserRepository,
        restaurant_repository: RestaurantRepository,
        menu_item_repository: MenuItemRepository,
        order_id: str,
        ) -> OrderResponse:

    order = await order_repository.get_by_id(order_id)
    if order is None:
        raise OrderNotFoundError(f"Order with id {order_id} not found.")

    return await _build_order_response(
        order, order_item_repository, user_repository, restaurant_repository, menu_item_repository
    )


async def query_orders(
        order_repository: OrderRepository,
        order_item_repository: OrderItemRepository,
        user_repository: UserRepository,
        restaurant_repository: RestaurantRepository,
        menu_item_repository: MenuItemRepository,
        customer_id: str | None = None,
        restaurant_id: str | None = None,
        status: OrderStatus | None = None,
        ) -> list[OrderResponse]:

    orders = await order_repository.get_orders(customer_id, restaurant_id, status)

    return [
        await _build_order_response(order, order_item_repository, user_repository, restaurant_repository, menu_item_repository)
        for order in orders
    ]