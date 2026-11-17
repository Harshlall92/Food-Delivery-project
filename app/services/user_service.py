from FoodDeliveryProject.app.repositories.restaurant_repository import RestaurantRepository
from FoodDeliveryProject.app.services.menu_item_service import RestaurantNotFoundError
from app.services.exceptions import UserNotFoundError, DuplicateItemError
from app.repositories.user_repository import UserRepository
from app.schemas.user import Customer, RestaurantOwner, RestaurantOwnerUpdate, UserCreate, UserUpdate

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

async def create_restaurant_owner(repository: UserRepository, data: UserCreate) -> RestaurantOwner:
    if await repository.contains_email(data.email):
        raise DuplicateItemError(f"Restaurant owner with email {data.email} already exists.")
    owner = RestaurantOwner(**data.model_dump())
    await repository.add_record(owner)
    return owner

async def update_restaurant_owner(user_repository: UserRepository, restaurant_repository: RestaurantRepository, owner_id: str, data: RestaurantOwnerUpdate) -> RestaurantOwner:
    owner = await user_repository.get_by_id(owner_id)
    if owner is None:
        raise UserNotFoundError(f"Restaurant owner with ID {owner_id} not found.")

    if data.restaurant_id is not None:
        restaurant = await restaurant_repository.get_by_id(data.restaurant_id)
        if restaurant is None:
            raise RestaurantNotFoundError(f"Restaurant with ID {data.restaurant_id} does not exist.")

    changes = data.model_dump(exclude_unset=True)
    updated = RestaurantOwner(**{**owner, **changes})

    if await user_repository.contains_email(updated.email) and updated.email != owner["email"]:
        raise DuplicateItemError(f"Restaurant owner with email {updated.email} already exists.")

    await user_repository.update_record(owner_id, updated)

    return updated