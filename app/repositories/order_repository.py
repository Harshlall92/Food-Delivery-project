from app.repositories.base_repository import BaseRepository
from app.schemas.order import Order, OrderStatus

FILE_PATH = "data/orders.json"

class OrderRepository(BaseRepository[Order]):

    def __init__(self):
        super().__init__(file_path=FILE_PATH, model=Order)

    async def get_orders_by_customer_id(self, customer_id: str) -> list[Order]:
        return [order for order in await self.get_all() if order.customer_id == customer_id]

    async def get_orders_by_restaurant_id(self, restaurant_id: str) -> list[Order]:
        return [order for order in await self.get_all() if order.restaurant_id == restaurant_id]

    async def get_orders_by_status(self, status: OrderStatus) -> list[Order]:
        return [order for order in await self.get_all() if order.status == status]