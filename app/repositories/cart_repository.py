from app.repositories.exceptions import RecordNotFoundError
from app.repositories.base_repository import BaseRepository
from app.schemas.cart import Cart

FILE_PATH = "data/carts.json"

class CartRepository(BaseRepository[Cart]):

    def __init__(self):
        super().__init__(file_path=FILE_PATH)

    async def has_cart_for_user(self, user_id: str) -> bool:
        try:
            await self.get_by_id(user_id)
            return True
        except RecordNotFoundError:
            return False

    async def get_cart_by_customer_id(self, customer_id: str) -> dict | None:
        for cart in await self.get_all():
            if cart.get("id") == customer_id:
                return cart
        return None