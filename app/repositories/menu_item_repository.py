from app.repositories.base_repository import BaseRepository
from app.schemas.menu_item import MenuItem
from app.repositories.exceptions import MenuItemNotFoundError

FILE_PATH = "data/menu-items.json"


class MenuItemRepository(BaseRepository[MenuItem]):

    def __init__(self):
        super().__init__(file_path=FILE_PATH, model=MenuItem)

    async def get_menu_items_by_restaurant_id(self, restaurant_id: str) -> list[MenuItem]:
        return [
            item
            for item in await self.get_all()
            if item.restaurant_id == restaurant_id
        ]

    async def get_menu_item_name_by_id(self, menu_item_id: str) -> str:
        item = await self.get_by_id(menu_item_id)
        if item is None:
            raise MenuItemNotFoundError(MenuItem, menu_item_id)
        return item.name