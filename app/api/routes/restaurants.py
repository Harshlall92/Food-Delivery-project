from fastapi import APIRouter,status
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.restaurant import *
import app.services.restaurant_service as rService

router = APIRouter(prefix = "/restaurants")


@router.get("", response_model=list[Restaurant])
async def get_restaurants():
    return await rService.get_restaurants(RestaurantRepository())

@router.post("",response_model=Restaurant, status_code = status.HTTP_201_CREATED  )
async def create_restaurants(payload: RestaurantInput):
    return await rService.create_restaurants(RestaurantRepository(), payload)