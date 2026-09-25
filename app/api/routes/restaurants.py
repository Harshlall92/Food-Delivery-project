from fastapi import FastAPI, APIRouter
from app.services import restaurant_service as rService
from app.schemas.restaurant import Restaurant

router = APIRouter(prefix = "/restaurants")

@router.get("", response_model=list[Restaurant])
async def get_restaurants():
    return await rService.get_restaurants()