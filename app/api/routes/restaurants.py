from fastapi import FastAPI, APIRouter
from app.services import restaurant_service as rService
from app.schemas.restaurant import Restaurant

router = APIRouter(prefix = "/restaurants")

@router.get("", response_model=list[Restaurant])
async def get_restaurants():
    return await rService.get_restaurants()
"""router.post to take the user input via an endpopint, /createRestaurant using the restaurant schema
pass the payload attributes using try catch statements, pass it to the createRestaurant(same function) in services"""