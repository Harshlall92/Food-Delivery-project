from app.schemas.cart import *

from app.schemas.order import Order, OrderItem

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

def create_test_order(
        customer_id: str = "test_customer_001",
        restaurant_id: str = "test_restaurant_001",
        status: str = "pending",
        total: Decimal | str = "10.00"
        ) -> Order:
    return Order(
        customer_id=customer_id,
        restaurant_id=restaurant_id,
        status=status,
        total=total if isinstance(total, Decimal) else Decimal(total)
    )

def create_test_order_item(
        order_id: str = "test_order_001",
        menu_item_id: str = "test_menu_item_001",
        quantity: int = 1,
        price_per_item: Decimal | str = "10.00"
        ) -> OrderItem:
    return OrderItem(
        order_id=order_id,
        menu_item_id=menu_item_id,
        quantity=quantity,
        price_per_item=price_per_item if isinstance(price_per_item, Decimal) else Decimal(price_per_item)
    )