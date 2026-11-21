from fastapi import APIRouter, HTTPException, status

from app.repositories.cart_repository import CartRepository
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.order_item_repository import OrderItemRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.user_repository import UserRepository
from app.schemas.order import Order, OrderCreate, OrderResponse, OrderStatus, OrderStatusUpdate
from app.services import order_service as oService
from app.services.exceptions import (
    CartNotFoundError,
    CartRestaurantMismatchError,
    CustomerNotFoundError,
    EmptyCartCheckoutError,
    InactiveMenuItemError,
    InactiveRestaurantError,
    InactiveUserError,
    InvalidOrderStatusError,
    InvalidRoleError,
    ItemNotFoundError,
    MenuItemNotFoundError,
    OrderNotFoundError,
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
        404: {"description": "The customer not found or has no active cart"},
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

@router.patch(
    "/{order_id}/status",
    response_model=Order,
    summary="Update an order's status",
    description="Sets the status of an existing order and returns the updated order.",
    responses={
        200: {"description": "Order status updated"},
        404: {"description": "The order does not exist"},
        422: {"description": "The status is invalid or the request is malformed"},
    },
)
async def update_order_status(order_id: str, data: OrderStatusUpdate):
    try:
        return await oService.update_order_status(OrderRepository(), order_id, data)
    except OrderNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidOrderStatusError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))

@router.get(
    "",
    response_model=list[OrderResponse],
    summary="List orders",
    description="Returns all orders, filtered by any combination of customer, restaurant, and status.",
    responses={
        200: {"description": "Matching orders (an empty list if none match)"},
        422: {"description": "A query parameter or status value is invalid"},
    },
)
async def query_orders(customer_id: str | None = None, restaurant_id: str | None = None, status: OrderStatus | None = None):
    return await oService.query_orders(
        OrderRepository(), OrderItemRepository(), UserRepository(), RestaurantRepository(), MenuItemRepository(),
        customer_id, restaurant_id, status,
    )

@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    summary="Get an order",
    description="Returns an order with its customer name, restaurant name, and items.",
    responses={
        200: {"description": "The order"},
        404: {"description": "The order does not exist"},
    },
)
async def get_order(order_id: str):
    try:
        return await oService.get_order(
            OrderRepository(), OrderItemRepository(), UserRepository(), RestaurantRepository(), MenuItemRepository(),
            order_id,
        )
    except ItemNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))