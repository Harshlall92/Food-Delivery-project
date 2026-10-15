from app.repositories.base_repository import BaseRepository
from app.schemas.restaurant import MenuItem, MenuItemInput

FILE_PATH = "data/menuItems.json"


class MenuItemRepository(BaseRepository[MenuItem]):

    def __init__(self):
        super().__init__(file_path=FILE_PATH)