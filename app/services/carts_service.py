from decimal import Decimal

from app.repositories.cart_repository import CartRepository
from app.repositories.exceptions import RecordNotFoundError
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.user_repository import UserRepository
from app.schemas.cart import Cart, CartCreate, CartItem
from app.services.exceptions import (
    CustomerNotFoundError,
    DuplicateCartError,
    InactiveMenuItemError,
    InactiveUserError,
    InvalidRoleError,
    MenuItemNotFoundError,
)


def _to_price(value) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"))


async def create_cart(
        cart_repository: CartRepository,
        user_repository: UserRepository,
        menu_item_repository: MenuItemRepository,
        restaurant_repository: RestaurantRepository,
        data: CartCreate,
        ) -> Cart:
    
    try:
        user = await user_repository.get_by_id(data.customer_id)
    except RecordNotFoundError as e:
        raise CustomerNotFoundError(f"Customer with id {data.customer_id} not found.") from e

   
    if user.get("role") != "customer":
        raise InvalidRoleError(f"User with id {data.customer_id} is not a customer.")

    
    if not user.get("active", False):
        raise InactiveUserError(f"Customer with id {data.customer_id} is not active.")

   
    if await cart_repository.get_active_cart_by_customer_id(data.customer_id) is not None:
        raise DuplicateCartError(f"Customer with id {data.customer_id} already has an active cart.")

    
    try:
        menu_item = await menu_item_repository.get_by_id(data.menu_item_id)
    except RecordNotFoundError as e:
        raise MenuItemNotFoundError(f"Menu item with id {data.menu_item_id} not found.") from e

    
    if not menu_item.get("available", False):
        raise InactiveMenuItemError(f"Menu item with id {data.menu_item_id} is not available.")

    
    restaurant_id = menu_item["restaurant_id"]
    try:
        restaurant_active = await restaurant_repository.is_restaurant_active(restaurant_id)
    except RecordNotFoundError:
        restaurant_active = False
    if not restaurant_active:
        raise InactiveMenuItemError(
            f"Menu item with id {data.menu_item_id} belongs to a restaurant that is not active."
        )

    
    price = _to_price(menu_item["price"])
    cart = Cart(
        customer_id=data.customer_id,
        restaurant_id=restaurant_id,
        items=[CartItem(menu_item_id=data.menu_item_id, quantity=data.quantity, price=price)],
        subtotal=price * data.quantity,
    )

    await cart_repository.add_record(cart)
    return cart