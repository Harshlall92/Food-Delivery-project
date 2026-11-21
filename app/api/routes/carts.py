from fastapi import APIRouter
from fastapi import APIRouter, HTTPException, status

import app.services.carts_service as cService
from app.repositories.cart_repository import CartRepository
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.user_repository import UserRepository
from app.schemas.cart import Cart, CartCreate, CartResponse
from app.services.exceptions import (
    CartNotFoundError,
    ItemNotFoundError,
    CustomerNotFoundError,
    DuplicateCartError,
    InactiveMenuItemError,
    InactiveUserError,
    InvalidRoleError,
    MenuItemNotFoundError,
)
from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, status

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
            404: {"description": "Customer or Menu item not found"},
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
    except (InvalidRoleError, InactiveUserError) as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except (MenuItemNotFoundError, CustomerNotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DuplicateCartError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except InactiveMenuItemError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))


@router.delete(
        "/{customer_id}",
        description="Delete a customer's active cart",
        responses={
            204: {"description": "Cart deleted successfully"},
            404: {"description": "Cart not found"},
        },
        status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_cart(customer_id: str):
    deleted = await cService.delete_cart(CartRepository(), customer_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cart for customer with id {customer_id} not found.",
        )

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
async def get_cart(customer_id: Annotated[str, Path(min_length=36, max_length=36)]):
    try:
        return await cService.retrieve_cart(
            CartRepository(), RestaurantRepository(), MenuItemRepository(), customer_id
        )
    except (CartNotFoundError, ItemNotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
