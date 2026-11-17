from FoodDeliveryProject.app.repositories.base_repository import BaseRepository
from FoodDeliveryProject.app.schemas.user import AnyUser


FILE_PATH = "data/users.json"

class UserRepository(BaseRepository[AnyUser]):

    def __init__(self):
        super().__init__(file_path=FILE_PATH)
