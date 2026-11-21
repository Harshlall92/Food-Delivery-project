from app.repositories.base_repository import BaseRepository
from app.schemas.cart import Cart

FILE_PATH = "data/carts.json"

class CartRepository(BaseRepository[Cart]):

    def __init__(self):
        super().__init__(file_path=FILE_PATH, model=Cart)

    async def has_cart_for_user(self, user_id: str) -> bool:
        return await self.get_by_id(user_id) is not None

    async def get_cart_by_customer_id(self, customer_id: str) -> Cart | None:
        return await self.get_by_id(customer_id)

    async def get_active_cart_by_customer_id(self, customer_id: str) -> Cart | None:
        return await self.get_by_id(customer_id)