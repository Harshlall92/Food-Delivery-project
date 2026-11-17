from app.services.exceptions import UserNotFoundError, DuplicateItemError
from app.repositories.user_repository import UserRepository
from app.schemas.user import Customer, UserCreate, UserUpdate

async def create_customer(repository: UserRepository, data: UserCreate) -> Customer:
    if await repository.contains_email(data.email):
        raise DuplicateItemError(f"Customer with email {data.email} already exists.")
    customer = Customer(**data.model_dump())
    await repository.add_record(customer)
    return customer

async def update_customer(repository: UserRepository, customer_id: str, data: UserUpdate) -> Customer:
    customer = await repository.get_by_id(customer_id)
    if customer is None:
        raise UserNotFoundError(f"Customer with ID {customer_id} not found.")

    changes = data.model_dump(exclude_unset=True)
    updated = Customer(**{**customer, **changes})

    if await repository.contains_email(updated.email) and updated.email != customer["email"]:
        raise DuplicateItemError(f"Customer with email {updated.email} already exists.")

    await repository.update_record(customer_id, updated)

    return updated