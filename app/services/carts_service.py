from decimal import Decimal

from app.repositories.cart_repository import CartRepository
from app.repositories.exceptions import MenuItemNotFoundError as RepoMenuItemNotFoundError
from app.repositories.exceptions import RestaurantNotFoundError
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.cart import Cart, CartItem, CartItemAdd, CartItemResponse, CartResponse
from app.services.exceptions import *

async def add_item_to_cart(
        cart_repository: CartRepository,
        menu_item_repository: MenuItemRepository,
        customer_id: str,
        cart_item_add: CartItemAdd,
        ) -> Cart:

    cart = await cart_repository.get_cart_by_customer_id(customer_id)
    if cart is None:
        raise CartNotFoundError(f"No active cart found for customer {customer_id}.")

    menu_item = await menu_item_repository.get_by_id(cart_item_add.menu_item_id)
    if menu_item is None:
        raise MenuItemNotFoundError(f"Menu item with id {cart_item_add.menu_item_id} not found.")

    if menu_item.restaurant_id != cart.restaurant_id:
        raise InvalidMenuItemError(
            f"Menu item with id {cart_item_add.menu_item_id} does not belong to the same restaurant as the cart."
        )

    if not menu_item.available:
        raise InactiveMenuItemError(f"Menu item with id {cart_item_add.menu_item_id} is not available.")

    items = list(cart.items)
    for i, item in enumerate(items):
        if item.menu_item_id == cart_item_add.menu_item_id:
            items[i] = item.model_copy(update={"quantity": item.quantity + cart_item_add.quantity})
            break
    else:
        items.append(CartItem(
            menu_item_id=cart_item_add.menu_item_id,
            quantity=cart_item_add.quantity,
            price=Decimal(str(menu_item.price)).quantize(Decimal("0.01")),
        ))

    subtotal = sum((item.price * item.quantity for item in items), Decimal("0.00"))

    updated_cart = Cart(
        customer_id=cart.customer_id,
        restaurant_id=cart.restaurant_id,
        items=items,
        subtotal=subtotal,
    )
    await cart_repository.update_record(customer_id, updated_cart)
    return updated_cart
    
from app.repositories.exceptions import RecordNotFoundError
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.user_repository import UserRepository
from app.schemas.cart import Cart, CartCreate, CartItem, CartResponse
from app.services.exceptions import (
    CustomerNotFoundError,
    DuplicateCartError,
    InactiveMenuItemError,
    InactiveUserError,
    InvalidRoleError,
    MenuItemNotFoundError,
)
from app.repositories.exceptions import MenuItemNotFoundError as RepoMenuItemNotFoundError
from app.repositories.exceptions import RestaurantNotFoundError as RepoRestaurantNotFoundError
from app.schemas.cart import CartItemResponse, CartResponse
from app.services.exceptions import CartNotFoundError, ItemNotFoundError


def _to_price(value) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"))


async def create_cart(
        cart_repository: CartRepository,
        user_repository: UserRepository,
        menu_item_repository: MenuItemRepository,
        restaurant_repository: RestaurantRepository,
        data: CartCreate,
        ) -> Cart:
    
    user = await user_repository.get_by_id(data.customer_id)
    if user is None:
        raise CustomerNotFoundError(f"Customer with id {data.customer_id} not found.")

    if user.role != "customer":
        raise InvalidRoleError(f"User with id {data.customer_id} is not a customer.")

    if not user.active:
        raise InactiveUserError(f"Customer with id {data.customer_id} is not active.")

    if await cart_repository.get_by_id(data.customer_id) is not None:
        raise DuplicateCartError(f"Customer with id {data.customer_id} already has an active cart.")

    menu_item = await menu_item_repository.get_by_id(data.menu_item_id)
    if menu_item is None:
        raise MenuItemNotFoundError(f"Menu item with id {data.menu_item_id} not found.")

    if not menu_item.available:
        raise InactiveMenuItemError(f"Menu item with id {data.menu_item_id} is not available.")

    restaurant_id = menu_item.restaurant_id
    try:
        restaurant_active = await restaurant_repository.is_restaurant_active(restaurant_id)
    except RecordNotFoundError:
        restaurant_active = False
    if not restaurant_active:
        raise InactiveMenuItemError(
            f"Menu item with id {data.menu_item_id} belongs to a restaurant that is not active."
        )

    price = _to_price(menu_item.price)
    cart = Cart(
        customer_id=data.customer_id,
        restaurant_id=restaurant_id,
        items=[CartItem(menu_item_id=data.menu_item_id, quantity=data.quantity, price=price)],
        subtotal=price * data.quantity,
    )

    await cart_repository.add_record(cart)
    return cart


async def delete_cart(cart_repository: CartRepository, customer_id: str) -> bool:
    return await cart_repository.delete_record(customer_id)

async def retrieve_cart(
    cart_repository: CartRepository,
    restaurant_repository: RestaurantRepository,
    menu_item_repository: MenuItemRepository,
    customer_id: str,
    ) -> CartResponse:

    cart = await cart_repository.get_by_id(customer_id)
    if cart is None:
        raise CartNotFoundError(f"No active cart found for customer {customer_id}.")

    try:
        restaurant_name = await restaurant_repository.get_restaurant_name_by_id(cart.restaurant_id)

        items: list[CartItemResponse] = []
        for item in cart.items:
            menu_item_name = await menu_item_repository.get_menu_item_name_by_id(item.menu_item_id)
            items.append(CartItemResponse(
                menu_item_name=menu_item_name,
                quantity=item.quantity,
                price=item.price,
            ))
    except (RepoRestaurantNotFoundError, RepoMenuItemNotFoundError) as e:
        raise ItemNotFoundError(e.message) from e

    total_quantity = sum(i.quantity for i in items)
    sub_total = sum((i.price * i.quantity for i in items), Decimal("0.00"))

    return CartResponse(
        restaurant_name=restaurant_name,
        items=items,
        total_quantity=total_quantity,
        sub_total=sub_total,
    )
