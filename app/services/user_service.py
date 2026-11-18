from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.exceptions import RecordNotFoundError
from app.services.exceptions import InvalidCredentialsError, ItemNotFoundError, DuplicateItemError
from app.repositories.user_repository import UserRepository
from app.schemas.user import Customer, CustomerAddress, RestaurantOwner, RestaurantOwnerUpdate, UserCreate, UserUpdate

async def create_customer(repository: UserRepository, data: UserCreate) -> Customer:
    if await repository.contains_email(data.email):
        raise DuplicateItemError(f"User with email {data.email} already exists.")
    customer = Customer(**data.model_dump())
    await repository.add_record(customer)
    return customer

async def update_customer(repository: UserRepository, customer_id: str, data: UserUpdate) -> Customer:
    try:
        customer = await repository.get_by_id(customer_id)
    except RecordNotFoundError as e:
        raise ItemNotFoundError(e.message) from e

    changes = data.model_dump(exclude_unset=True)

    updated = Customer(**{**customer, **changes})

    if await repository.contains_email(updated.email) and updated.email != customer["email"]:
        raise DuplicateItemError(f"User with email {updated.email} already exists.")

    await repository.update_record(customer_id, updated)

    return updated

async def add_customer_address(repository: UserRepository, customer_id: str, address: CustomerAddress) -> Customer:
    try:
        customer = await repository.get_by_id(customer_id)
    except RecordNotFoundError as e:
        raise ItemNotFoundError(e.message) from e

    if customer["role"] != "customer":
        raise InvalidCredentialsError(f"User with id {customer_id} is not a customer.")

    for addr in customer["addresses"]:
        if addr["label"] == address.label:
            raise DuplicateItemError(f"Address with label {address.label} already exists for this customer.")

    customer["addresses"].append(address)

    updated_customer = Customer(**customer)

    await repository.update_record(customer_id, updated_customer)

    return updated_customer

async def update_customer_address(repository: UserRepository, customer_id: str, address_label: str, new_address: CustomerAddress) -> Customer:
    try:
        customer = await repository.get_by_id(customer_id)
    except RecordNotFoundError as e:
        raise ItemNotFoundError(e.message) from e

    if customer["role"] != "customer":
        raise InvalidCredentialsError(f"User with id {customer_id} is not a customer.")

    address_found = False
    for i, addr in enumerate(customer["addresses"]):
        if addr["label"] == address_label:
            customer["addresses"][i] = new_address
            address_found = True
            break

    if not address_found:
        raise ItemNotFoundError(f"Address with label {address_label} not found for this customer.")

    updated_customer = Customer(**customer)

    await repository.update_record(customer_id, updated_customer)

    return updated_customer

async def create_restaurant_owner(repository: UserRepository, data: UserCreate) -> RestaurantOwner:
    if await repository.contains_email(data.email):
        raise DuplicateItemError(f"User with email {data.email} already exists.")
    owner = RestaurantOwner(**data.model_dump())
    await repository.add_record(owner)
    return owner

async def update_restaurant_owner(user_repository: UserRepository, restaurant_repository: RestaurantRepository, owner_id: str, data: RestaurantOwnerUpdate) -> RestaurantOwner:
    try:
        owner = await user_repository.get_by_id(owner_id)
    except RecordNotFoundError as e:
        raise ItemNotFoundError(e.message) from e

    if data.restaurant_id is not None:
        try:
            await restaurant_repository.get_by_id(data.restaurant_id)
        except RecordNotFoundError as e:
            raise ItemNotFoundError(e.message) from e

    changes = data.model_dump(exclude_unset=True)
    updated = RestaurantOwner(**{**owner, **changes})

    if await user_repository.contains_email(updated.email) and updated.email != owner["email"]:
        raise DuplicateItemError(f"User with email {updated.email} already exists.")

    await user_repository.update_record(owner_id, updated)

    return updated