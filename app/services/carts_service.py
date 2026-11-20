from decimal import Decimal

from app.repositories.cart_repository import CartRepository
from app.repositories.exceptions import MenuItemNotFoundError, RestaurantNotFoundError
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.cart import CartItemResponse, CartResponse
from app.services.exceptions import CartNotFoundError, ItemNotFoundError

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
        restaurant_name = await restaurant_repository.get_restaurant_name_by_id(cart["restaurant_id"])

        items: list[CartItemResponse] = []
        for item in cart.get("items", []):
            menu_item_name = await menu_item_repository.get_menu_item_name_by_id(item["menu_item_id"])
            items.append(CartItemResponse(
                menu_item_name=menu_item_name,
                quantity=item["quantity"],
                price_per_item=Decimal(str(item["price"])),
            ))
    except (RestaurantNotFoundError, MenuItemNotFoundError) as e:
        raise ItemNotFoundError(e.message) from e

    total_quantity = sum(i.quantity for i in items)
    sub_total = sum((i.price_per_item * i.quantity for i in items), Decimal("0.00"))

    return CartResponse(
        restaurant_name=restaurant_name,
        items=items,
        total_quantity=total_quantity,
        sub_total=sub_total,
    )