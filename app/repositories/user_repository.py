from FoodDeliveryProject.app.repositories.base_repository import BaseRepository
from FoodDeliveryProject.app.schemas.user import User


FILE_PATH = "data/users.json"

class UserRepository(BaseRepository[User]):

    def __init__(self):
        super().__init__(file_path=FILE_PATH)
