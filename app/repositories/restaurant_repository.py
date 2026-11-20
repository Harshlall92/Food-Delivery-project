from app.repositories.base_repository import BaseRepository
from app.schemas.restaurant import Restaurant

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