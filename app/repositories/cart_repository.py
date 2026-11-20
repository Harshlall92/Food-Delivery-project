from app.repositories.exceptions import RecordNotFoundError
from app.repositories.base_repository import BaseRepository
from app.schemas.cart import Cart
from typing import Optional

FILE_PATH = "data/cart.json"

class CartRepository(BaseRepository[Cart]):

    def __init__(self):
        super().__init__(file_path=FILE_PATH)

    async def has_cart_for_user(self, user_id: str) -> bool:
        try:
            await self.get_by_id(user_id)
            return True
        except RecordNotFoundError:
            return False

    
    async def get_active_cart_by_customer_id(self, customer_id: str) -> Optional[Cart]:
        try:
            record = await self.get_by_id(customer_id)
        except RecordNotFoundError:
            return None
        # Carts are stored with the customer id under the "id" key
        return Cart.model_validate({**record, "customer_id": record["id"]})