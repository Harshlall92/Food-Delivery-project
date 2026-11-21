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
    
async def retrieve_cart(
    cart_repository: CartRepository,
    restaurant_repository: RestaurantRepository,
    menu_item_repository: MenuItemRepository,
    customer_id: str,
    ) -> CartResponse:
    
    cart = await cart_repository.get_cart_by_customer_id(customer_id)
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
    except (RestaurantNotFoundError, RepoMenuItemNotFoundError) as e:
        raise ItemNotFoundError(e.message) from e

    total_quantity = sum(i.quantity for i in items)
    sub_total = sum((i.price * i.quantity for i in items), Decimal("0.00"))

    return CartResponse(
        restaurant_name=restaurant_name,
        items=items,
        total_quantity=total_quantity,
        sub_total=sub_total,
    )
