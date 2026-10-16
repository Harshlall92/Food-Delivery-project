from app.repositories.base_repository import BaseRepository
from app.schemas.menu_item import MenuItem

FILE_PATH = "data/menu-items.json"


class MenuItemRepository(BaseRepository[MenuItem]):

    def __init__(self):
        super().__init__(file_path=FILE_PATH)

    async def get_menu_items_by_restaurant_id(self, restaurant_id: str) -> list[dict]:
        return [
            item
            for item in await self.get_all()
            if item["restaurant_id"] == restaurant_id
        ]