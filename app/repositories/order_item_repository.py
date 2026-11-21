from app.repositories.base_repository import BaseRepository
from app.schemas.order import OrderItem

FILE_PATH = "data/order-items.json"

class OrderItemRepository(BaseRepository[OrderItem]):

    def __init__(self):
        super().__init__(file_path=FILE_PATH, model=OrderItem)

    async def get_items_by_order_id(self, order_id: str) -> list[OrderItem]:
        return [item for item in await self.get_all() if item.order_id == order_id]

    async def add_order_items(self, items: list[OrderItem]) -> list[OrderItem]:
        for item in items:
            await self.add_record(item)
        return items