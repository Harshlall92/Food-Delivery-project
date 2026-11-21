from app.schemas.cart import Cart,CartItemAdd, CartItem
from app.services.exceptions import *
from decimal import Decimal
from app.repositories.cart_repository import CartRepository
from app.repositories.exceptions import MenuItemNotFoundError, RestaurantNotFoundError
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.cart import CartItemResponse, CartResponse
from app.services.exceptions import CartNotFoundError, ItemNotFoundError

async def add_item_to_cart(
        cart_repo: CartRepository,
        menu_repo: MenuItemRepository,
        customer_id: str, 
        cart_item_add: CartItemAdd) -> Cart:
    cart = await cart_repo.get_by_id(customer_id)
    if cart is None:
            raise CartNotFoundError()
    
    menu_item = await menu_repo.get_menu_items_by_restaurant_id(cart["restaurant_id"])
    
    if menu_item is None or menu_item.restaurant_id != cart.restaurant_id:
        raise MenuItemNotFound()
    if not menu_item["available"] :
        raise InactiveMenuItemError()

    for i, item in enumerate(list(cart.items)):
        if item.menu_item_id == cart_item_add.menu_item_id:
            list(cart.items)[i] = item.model_copy(update={"quantity": item.quantity + cart_item_add.quantity})
            break
    else:
        list(cart.items).append(CartItem(
            menu_item_id=cart_item_add.menu_item_id,
            quantity=cart_item_add.quantity,
            price=Decimal(str(menu_item.price)).quantize(Decimal("0.01"))
        ))
    
    subtotal = sum((item.price * item.quantity for item in list(cart.items)), Decimal("0.00"))
    update = Cart(customer_id=customer_id, 
        restaurant_id=cart["restaurant_id"],
        items=cart["items"],
        subtotal=subtotal)
    await cart_repo.update_record(customer_id, update)
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
