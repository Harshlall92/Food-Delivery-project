from fastapi import APIRouter, HTTPException, status

from app.repositories.cart_repository import CartRepository
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.order_item_repository import OrderItemRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.user_repository import UserRepository
from app.schemas.order import Order, OrderCreate
from app.services import order_service as oService
from app.services.exceptions import (
    CartNotFoundError,
    CartRestaurantMismatchError,
    CustomerNotFoundError,
    EmptyCartCheckoutError,
    InactiveMenuItemError,
    InactiveRestaurantError,
    InactiveUserError,
    InvalidRoleError,
    MenuItemNotFoundError,
    RestaurantNotFoundError,
)

router = APIRouter(
    prefix="/api/orders",
    tags=["orders"],
)


@router.post(
    "",
    response_model=Order,
    status_code=status.HTTP_201_CREATED,
    summary="Checkout a customer's cart",
    description="Creates an order from the customer's cart using current menu prices, then deletes the cart.",
    responses={
        201: {"description": "Order created"},
        404: {"description": "The customer is unavailable or has no active cart"},
        409: {"description": "A cart item belongs to a different restaurant than the cart"},
        422: {"description": "Pydantic validation error, empty cart, or the restaurant or a menu item is missing or inactive"},
    },
)
async def checkout_cart(data: OrderCreate):
    try:
        return await oService.checkout_cart(
            OrderRepository(), OrderItemRepository(), CartRepository(),
            UserRepository(), RestaurantRepository(), MenuItemRepository(), data,
        )
    except (CustomerNotFoundError, InvalidRoleError, InactiveUserError, CartNotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except CartRestaurantMismatchError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except (EmptyCartCheckoutError, RestaurantNotFoundError, InactiveRestaurantError,
            MenuItemNotFoundError, InactiveMenuItemError) as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))