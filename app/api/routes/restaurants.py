from unittest import result

from fastapi import APIRouter,status, HTTPException
from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.menu_item_repository import MenuItemRepository
from app.schemas.restaurant import *
import app.services.restaurant_service as rService
import app.services.menu_item_service as mService

router = APIRouter(prefix = "/api/restaurants")


@router.get("", response_model=list[Restaurant])
async def get_restaurants():
    return await rService.get_restaurants(RestaurantRepository())

@router.get("/search", response_model=list[Restaurant])
async def search_restaurants(name: str):
    return await rService.get_restaurants_by_name(RestaurantRepository(), name)

@router.get("/filter", response_model=list)
async def filter_restaurants(cuisine: str):
    return await rService.get_restaurants_by_cuisine(RestaurantRepository(), cuisine)

@router.post("", response_model=Restaurant, status_code = status.HTTP_201_CREATED)
async def create_restaurants(payload: RestaurantInput):
    return await rService.create_restaurants(RestaurantRepository(), payload)

@router.get(
    "/{restaurant_id}",
    response_model=FullRestaurantOutput,
    responses={404: {"description": "Restaurant not found"}},
    description="Retrieves the full details of a restaurant, including its name, address, cuisine, and menu items."
)
async def get_full_restaurant_info(restaurant_id: str):
    try:
        return await rService.get_full_restaurant_info(RestaurantRepository(), MenuItemRepository(), restaurant_id)
    except mService.RestaurantNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))