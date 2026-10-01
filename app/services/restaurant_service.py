from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.restaurant import Restaurant

class RestaurantService:

    repository: RestaurantRepository

    def __init__(self, repository: RestaurantRepository = RestaurantRepository()):
        self.repository = repository

    async def get_restaurants(self) -> list[Restaurant]:

        query = await self.repository.get_restaurants()

        return [
            self.validate_restaurant(restaurant)
            for restaurant in query
        ]

    def validate_restaurant(self, restaurant: dict) -> Restaurant:
       return Restaurant(**restaurant)
