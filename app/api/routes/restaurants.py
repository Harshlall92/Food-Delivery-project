from fastapi import FastAPI, APIRouter
from app.repositories.restaurant_repository import RestaurantRepository
from app.services.restaurant_service import RestaurantService
from app.schemas.restaurant import Restaurant

router = APIRouter(prefix = "/restaurants")

service = RestaurantService()


@router.get("", response_model=list[Restaurant])
async def get_restaurants():
    return await service.get_restaurants()