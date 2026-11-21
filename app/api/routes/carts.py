from fastapi import APIRouter, HTTPException, status
from app.services import carts_service as cService 
from app.services.exceptions import *
from app.repositories.cart_repository import CartRepository
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.cart import CartResponse,CartItemAdd, Cart

router = APIRouter(
    prefix="/api/carts",
    tags=["carts"],
)

@router.post(
    "/{customer_id}/items",
    response_model=Cart,
    summary="Add item to cart",
    description="Adds a menu item to the customer's cart, or increases its quantity if it is already in the cart.",
    responses={
        200: {"description": "Item added; returns the updated cart"},
        404: {"description": "The customer has no active cart, or the menu item does not exist"},
        422: {"description": "Pydantic validation error, the menu item is unavailable, or it belongs to a different restaurant"},
    },
)
async def add_item_to_cart(customer_id: str, payload: CartItemAdd):
    try:
        return await cService.add_item_to_cart(
            CartRepository(), MenuItemRepository(), customer_id, payload
        )
    except (CartNotFoundError, MenuItemNotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (InvalidMenuItemError, InactiveMenuItemError) as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))
        
@router.get(
    "/{customer_id}",
    response_model=CartResponse,
    summary="Retrieve a customer's active cart",
    description="Returns the customer's cart with restaurant and menu item names and calculated totals.",
    responses={
        404: {"description": "The customer does not have an active cart"},
        422: {"description": "Pydantic validation error"},
    },
)
async def get_cart(customer_id: str):
    try:
        return await cService.retrieve_cart(
            CartRepository(), RestaurantRepository(), MenuItemRepository(), customer_id
        )
    except (CartNotFoundError, ItemNotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
