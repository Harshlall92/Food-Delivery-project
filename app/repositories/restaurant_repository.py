from app.repositories.base_repository import BaseRepository
from app.schemas.restaurant import Restaurant
from app.repositories.exceptions import RecordNotFoundError, RestaurantNotFoundError

FILE_PATH = "data/restaurants.json"

class RestaurantRepository(BaseRepository[Restaurant]):

    def __init__(self):
        super().__init__(file_path=FILE_PATH, model=Restaurant)

    async def get_by_name(self, name: str) -> list[Restaurant]:
        data = await self.get_all()

        return [
            restaurant
            for restaurant in data
            if name in restaurant.name
        ]

    async def get_by_cuisine(self, cuisine: str) -> list[Restaurant]:
        data = await self.get_all()
        
        return [
            restaurant
            for restaurant in data
            if restaurant.cuisine == cuisine
        ]

    async def get_all_cuisine(self) -> list[str]:
        data = await self.get_all()

        cuisines: list = []

        for restaurant in data:
            if restaurant.cuisine not in cuisines:
                cuisines.append(restaurant.cuisine)

        return cuisines

    async def get_restaurant_name_by_id(self, restaurant_id: str) -> str:
        restaurant = await self.get_by_id(restaurant_id)
        if restaurant is None:
            raise RestaurantNotFoundError(Restaurant, restaurant_id)
        return restaurant.name
    
    async def is_restaurant_active(self, restaurant_id: str) -> bool:
        restaurant = await self.get_by_id(restaurant_id)
        if restaurant is None:
            raise RecordNotFoundError(Restaurant, restaurant_id)
        return restaurant.active
