from fastapi import FastAPI, APIRouter
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.restaurant import Restaurant
import app.services.restaurant_service as rService

router = APIRouter(prefix = "/restaurants")


@router.get("", response_model=list[Restaurant])
async def get_restaurants():
    return await rService.get_restaurants(RestaurantRepository())
