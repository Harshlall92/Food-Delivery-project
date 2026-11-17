from app.repositories.user_repository import UserRepository
from app.schemas.user import Customer, UserCreate

async def create_customer(repository: UserRepository, data: UserCreate) -> Customer:
    customer = Customer(**data.model_dump())
    await repository.add_record(customer)
    return customer