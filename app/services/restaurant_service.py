from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.restaurant import Restaurant

async def get_restaurants(repository: RestaurantRepository) -> list[Restaurant]:

    query = await repository.get_restaurants()

    return [
        validate_restaurant(restaurant)
        for restaurant in query
    ]

def validate_restaurant(restaurant: dict) -> Restaurant:
    return Restaurant(**restaurant)
