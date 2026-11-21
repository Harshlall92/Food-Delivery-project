from app.repositories.base_repository import BaseRepository
from app.schemas.order import Order, OrderStatus

FILE_PATH = "data/orders.json"

class OrderRepository(BaseRepository[Order]):

    def __init__(self):
        super().__init__(file_path=FILE_PATH, model=Order)

    async def get_orders(
            self,
            customer_id: str | None = None,
            restaurant_id: str | None = None,
            status: OrderStatus | None = None,
            ) -> list[Order]:
        return [
            order for order in await self.get_all()
            if (customer_id is None or order.customer_id == customer_id)
            and (restaurant_id is None or order.restaurant_id == restaurant_id)
            and (status is None or order.status == status)
        ]

    async def get_orders_by_customer_id(self, customer_id: str) -> list[Order]:
        return await self.get_orders(customer_id=customer_id)

    async def get_orders_by_restaurant_id(self, restaurant_id: str) -> list[Order]:
        return await self.get_orders(restaurant_id=restaurant_id)

    async def get_orders_by_status(self, status: OrderStatus) -> list[Order]:
        return await self.get_orders(status=status)