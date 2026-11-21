from app.schemas.cart import Cart,CartItemAdd
from app.repositories import cart_repository as cRepo, menu_item_repository as mRepo
from app.services.exceptions import *
from decimal import Decimal
from app.repositories.cart_repository import CartRepository
from app.repositories.exceptions import MenuItemNotFoundError, RestaurantNotFoundError
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.cart import CartItemResponse, CartResponse
from app.services.exceptions import CartNotFoundError, ItemNotFoundError

async def add_item_to_cart(
        customer_id: str, 
        cart_item_add: CartItemAdd) -> Cart:
    cart = await cRepo.get_by_id(customer_id)
    menu_item = await mRepo.get_menu_items_by_restaurant_id(cart["restaurant_id"])
    menu_item = next(
        (m for m in menu_item if m["id"] == cart_item_add.menu_item_id), None
    )
    if menu_item is None:
        raise MenuItemNotFound
    if menu_item["available"] == False:
        raise InactiveMenuItemError
    if cart is None:
        raise CartNotFoundError

    for item in cart["items"]:
        if item["menu_item_id"] == cart_item_add.menu_item_id:
            item["quantity"] += cart_item_add.quantity
            break
        else:
            cart["items"].append({
                "menu_item_id":cart_item_add.menu_item_id,
                "quantity": cart_item_add.quantity,
                "price": menu_item["price"],
            }) 
        subtotal = sum(Decimal(str(i["price"])) * i["quantity"] for i in cart["items"])
        update = Cart(customer_id=customer_id, 
                      restaurant_id=cart["restaurant_id"],
                      items=cart["items"],
                      subtotal=subtotal)
        await cRepo.update_record(customer_id, update)
        return update
    
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
                price_per_item=item.price_per_item,
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
