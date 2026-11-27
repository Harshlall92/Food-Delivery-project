from typing_extensions import Literal

from app.schemas.cart import *

from app.schemas.order import Order, OrderItem, OrderStatus
from app.schemas.user import Admin, Customer, CustomerAddress, RestaurantOwner, AnyUser

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
        status: OrderStatus = "pending",
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

PASSWORD = "testpw"

def create_test_customer(
        *,
        email = "customer@example.com",
        password: str = PASSWORD,
        first_name: str = "Test",
        last_name: str = "User",
        addresses: list[CustomerAddress] | None = None,
        active: bool = True,
        payment_method: str | None = None
        ) -> Customer:
    return Customer(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        addresses=addresses or [],
        active=active,
        payment_method=payment_method
    )

def create_test_restaurant_owner(
        *,
        email: str = "test@example.com",
        password: str = PASSWORD,
        first_name: str = "Test",
        last_name: str = "User",
        active: bool = True,
        restaurant_id: str | None = None
        ) -> RestaurantOwner:
    return RestaurantOwner(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        active=active,
        restaurant_id=restaurant_id
    )

def create_test_admin(
        *,
        email: str = "admin@example.com",
        password: str = PASSWORD,
        first_name: str = "Test",
        last_name: str = "Admin",
        active: bool = True,
        permissions: list[str] | None = None 
) -> Admin:
    return Admin(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        active=active,
        permissions=permissions or []
    )

def create_user_with_role(role: Literal["customer", "restaurant_owner", "admin"], **kwargs) -> AnyUser:
    if role == "customer":
        return create_test_customer(**kwargs)
    elif role == "restaurant_owner":
        return create_test_restaurant_owner(**kwargs)
    elif role == "admin":
        return create_test_admin(**kwargs)
    else:
        raise ValueError(f"Invalid role: {role}")