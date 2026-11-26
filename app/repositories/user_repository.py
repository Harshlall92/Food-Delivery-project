from app.repositories.base_repository import BaseRepository
from app.repositories.exceptions import RecordNotFoundError
from app.schemas.user import AnyUser, User


FILE_PATH = "data/users.json"

class UserRepository(BaseRepository[AnyUser]):

    def __init__(self):
        super().__init__(file_path=FILE_PATH, model=AnyUser)

    async def contains_email(self, email: str) -> bool:
        data = await self.get_all()
        return any(user.email == email for user in data)

    async def get_by_email(self, email: str) -> AnyUser:
        data = await self.get_all()
        for user in data:
            if user.email == email:
                return user
        raise RecordNotFoundError(User, id=email)