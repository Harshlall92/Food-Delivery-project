from fastapi import APIRouter, HTTPException, status

from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.menu_item import MenuItem, MenuItemInput
import app.services.menu_item_service as mService

router = APIRouter(prefix="/api/restaurants/{restaurant_id}/menu-items", tags=["menu items"])


@router.post(
    "",
    response_model=MenuItem,
    status_code=status.HTTP_201_CREATED,
    summary="Add a menu item to a restaurant",
    description="Creates a new menu item for the restaurant with the given ID. "
    "The price must be greater than 0.",
    responses={
        404: {"description": "Restaurant not found"},
        422: {"description": "Invalid menu item data (e.g. empty name or price <= 0)"},
    },
)
async def create_menu_item(restaurant_id: str, payload: MenuItemInput):
    try:
        return await mService.create_menu_item(
            RestaurantRepository(), MenuItemRepository(), restaurant_id, payload
        )
    except mService.RestaurantNotFoundError as e:
        # Turn the service's error into an HTTP 404 response.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))