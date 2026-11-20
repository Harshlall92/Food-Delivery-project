from app.schemas.cart import Cart,CartItemAdd
from app.repositories import cart_repository as cRepo, menu_item_repository as mRepo
from app.services.exceptions import *
from app.repositories.exceptions import RecordNotFoundError
from decimal import Decimal

async def add_item_to_cart(
        customer_id: str, 
        cart_item_add: CartItemAdd) -> Cart:
    try:
        cart = await cRepo.get_by_id(customer_id)
        menu_item = await mRepo.get_menu_items_by_restaurant_id(cart["restaurant_id"])
    except RecordNotFoundError as e:
        raise ItemNotFoundError(e.message)
    menu_item = next(
        (m for m in menu_item if m["id"] == cart_item_add.menu_item_id), None
    )
    if menu_item is None:
        raise MenuItemNotFound
    elif menu_item["available"] == False:
        raise InactiveMenuItemError

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