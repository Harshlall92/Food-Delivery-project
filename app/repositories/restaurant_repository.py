from app.repositories.base_repository import BaseRepository
from app.schemas.restaurant import Restaurant

FILE_PATH = "data/restaurants.json"

class RestaurantRepository(BaseRepository[Restaurant]):

    def __init__(self):
        super().__init__(file_path=FILE_PATH)