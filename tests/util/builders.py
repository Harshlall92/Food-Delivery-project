from app.schemas.cart import *

def create_test_cart_item(
        menu_item_id: str = "test_menu_item_001",
        quantity: int = 1,
        price: Decimal | str = "9.99"
        ) -> CartItem:
    return CartItem(
        menu_item_id=menu_item_id,
        quantity=quantity,
        price=price if isinstance(price, Decimal) else Decimal(price)
    )

def create_test_cart(
        customer_id: str = "test_customer_001",
        restaurant_id: str = "test_restaurant_001",
        items: list[CartItem] = [],
        subtotal: Decimal | str = "9.99"
        ) -> Cart:
    return Cart(
        customer_id=customer_id,
        restaurant_id=restaurant_id,
        items=items,
        subtotal=subtotal if isinstance(subtotal, Decimal) else Decimal(subtotal)
    )

def create_test_cart_item_add(
        menu_item_id: str = "test_menu_item_001",
        quantity: int = 1
        ) -> CartItemAdd:
    return CartItemAdd(
        menu_item_id=menu_item_id,
        quantity=quantity
    )