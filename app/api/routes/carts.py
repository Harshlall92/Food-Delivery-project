from fastapi import APIRouter, HTTPException, status

from app.repositories.cart_repository import CartRepository
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.cart import CartResponse
from app.services import carts_service as cService
from app.services.exceptions import CartNotFoundError, ItemNotFoundError
from uuid import UUID

router = APIRouter(prefix="/api", tags=["carts"])


@router.get(
    "/cart/{customer_id}",
    response_model=CartResponse,
    summary="Retrieve a customer's active cart",
    description="Returns the customer's cart with restaurant and menu item names and calculated totals.",
    responses={
        404: {"description": "The customer does not have an active cart"},
        422: {"description": "Pydantic validation error"},
    },
)
async def get_cart(customer_id: UUID):
    try:
        return await cService.retrieve_cart(
            CartRepository(), RestaurantRepository(), MenuItemRepository(), str(customer_id)
        )
    except (CartNotFoundError, ItemNotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))