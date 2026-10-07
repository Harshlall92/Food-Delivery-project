from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.restaurant import *

async def get_restaurants(repository: RestaurantRepository) -> list[Restaurant]:

    query = await repository.get_all()

    return [
        validate_restaurant(restaurant)
        for restaurant in query
    ]

async def create_restaurants(repository: RestaurantRepository, data: RestaurantInput) -> Restaurant:
    record = Restaurant(**data.model_dump())

    await repository.add_record(record)

    return record



def validate_restaurant(restaurant: dict) -> Restaurant:
    return Restaurant(**restaurant)
