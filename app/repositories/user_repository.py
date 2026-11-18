from app.repositories.base_repository import BaseRepository
from app.schemas.user import AnyUser


FILE_PATH = "data/users.json"

class UserRepository(BaseRepository[AnyUser]):

    def __init__(self):
        super().__init__(file_path=FILE_PATH)

    async def contains_email(self, email: str) -> bool:
        data = await self.get_all()
        return any(user.get("email") == email for user in data)