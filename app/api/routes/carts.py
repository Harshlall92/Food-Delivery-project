from fastapi import APIRouter, HTTPException, status
from app.schemas.cart import CartItemAdd
from app.services import carts_service as cService 
from app.services.exceptions import ItemNotFoundError,CartNotFoundError
from app.repositories.cart_repository import CartRepository
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.cart import CartResponse
from uuid import UUID

router = APIRouter(
    prefix="/api/carts",
    tags=["carts"],
)

@router.post(
    "/cart/{customer_id}/items", 
    response_model = CartItemAdd,
    summary = "Add item to Cart",
    description = "Creates an item in the cart if it exists in the restaurant or increases quantity if already in cart",
    responses = {
        404: {"description": "Customer not found or Menu item does not exist"},
        422: {"description": "Invalid menu item data (e.g. empty name or price <= 0)"},
        200: {"description": "Item has been added successful"}
    },
)
async def add_menu_item(customer_id: str, payload: CartItemAdd):
    try: 
        return await cService.add_item_to_cart(
            customer_id, payload
        )
    except ItemNotFoundError as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = str(e))
    
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
