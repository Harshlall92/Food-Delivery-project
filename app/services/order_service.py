from decimal import Decimal

from app.repositories.cart_repository import CartRepository
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.order_item_repository import OrderItemRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.user_repository import UserRepository
from app.schemas.order import Order, OrderCreate, OrderItem
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
)


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