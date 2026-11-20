from app.repositories.base_repository import BaseRepository
from app.schemas.cart import Cart
from typing import Optional

FILE_PATH = "data/carts.json"

class CartRepository(BaseRepository[Cart]):

    def __init__(self):
        super().__init__(file_path=FILE_PATH, model=Cart)

    async def has_cart_for_user(self, user_id: str) -> bool:
        try:
            await self.get_by_id(user_id)
            return True
        except RecordNotFoundError:
            return False

    
