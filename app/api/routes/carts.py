from fastapi import APIRouter
from fastapi import APIRouter, HTTPException, status

import app.services.carts_service as cService
from app.repositories.cart_repository import CartRepository
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.user_repository import UserRepository
from app.schemas.cart import Cart, CartCreate
from app.services.exceptions import (
    CustomerNotFoundError,
    DuplicateCartError,
    InactiveMenuItemError,
    InactiveUserError,
    InvalidRoleError,
    MenuItemNotFoundError,
)

router = APIRouter(
    prefix="/api/carts",
    tags=["carts"],
)



@router.post(
        "",
        description="Create a new cart for a customer containing a first menu item",
        responses={
            201: {"description": "Cart created successfully"},
            401: {"description": "User is not an active customer"},
            404: {"description": "Menu item not found"},
            409: {"description": "Customer already has an active cart"},
            422: {"description": "Invalid input data or menu item is unavailable"},
        },
        status_code=status.HTTP_201_CREATED,
        response_model=Cart,
)
async def create_cart(data: CartCreate):
    try:
        return await cService.create_cart(
            CartRepository(),
            UserRepository(),
            MenuItemRepository(),
            RestaurantRepository(),
            data,
        )
    except (CustomerNotFoundError, InvalidRoleError, InactiveUserError) as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except MenuItemNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DuplicateCartError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except InactiveMenuItemError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))