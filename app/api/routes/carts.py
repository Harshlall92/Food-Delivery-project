from fastapi import APIRouter, HTTPException, status
from app.schemas.cart import CartItemAdd
from app.services import carts_service as cService 
from app.services.exceptions import ItemNotFoundError

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
    