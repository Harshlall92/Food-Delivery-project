import pytest

from app.services.exceptions import UserNotFoundError, DuplicateItemError
from app.schemas.user import Customer, UserCreate, UserUpdate
from app.services.user_service import *
from tests.util.helpers import create_user_file, create_user_repository, create_test_customer, create_test_restaurant_owner

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.fixture
def repository(tmp_path):
    return create_user_repository(create_user_file(tmp_path))

@pytest.mark.anyio
async def test_create_customer_account(repository):
    data = UserCreate(
        email="test@example.com",
        password="password123",
        confirm_password="password123",
        first_name="John",
        last_name="Doe"
    )

    result = await create_customer(repository, data)

    assert isinstance(result, Customer)
    assert result.email == data.email
    assert result.first_name == data.first_name
    assert result.last_name == data.last_name

    contents = await repository._read_file()

    assert len(contents) == 1

@pytest.mark.anyio
async def test_create_customer_raises_duplicate_error(repository):
    existing_customer = create_test_customer()
    await repository.add_record(existing_customer)

    data = UserCreate(
        email=existing_customer.email,
        password="password123",
        confirm_password="password123",
        first_name="Jane",
        last_name="Smith"
    )

    with pytest.raises(DuplicateItemError, match=f"Customer with email {existing_customer.email} already exists."):
        await create_customer(repository, data)

@pytest.mark.anyio
async def test_update_customer_account(repository):
    customer = create_test_customer()
    await repository.add_record(customer)

    customer_id = customer.id

    update_data = UserUpdate(
        email="new_email@test.com",
        password="newpassword",
        confirm_password="newpassword",
        first_name="Tim",
        last_name="Apple",
        active=False
    )

    result = await update_customer(repository, customer_id, update_data)

    assert isinstance(result, Customer)
    assert result.email == update_data.email
    assert result.first_name == update_data.first_name
    assert result.last_name == update_data.last_name
    assert result.active == update_data.active

    updated = await repository.get_by_id(customer_id)

    assert updated is not None
    assert updated["email"] == update_data.email
    assert updated["password"] != customer.password  # Password should be hashed and different
    assert updated["first_name"] == update_data.first_name
    assert updated["last_name"] == update_data.last_name
    assert updated["active"] == update_data.active

@pytest.mark.anyio
async def test_update_customer_raises_user_not_found_error_on_nonexistent_user(repository):

    non_existent_id = "non-existent-id"

    update_data = UserUpdate(
        email="new_email@test.com",
        password="newpassword",
        confirm_password="newpassword",
        first_name="Tim",
        last_name="Apple",
        active=False
    )

    with pytest.raises(UserNotFoundError, match=f"Customer with ID {non_existent_id} not found."):
        await update_customer(repository, non_existent_id, update_data)

@pytest.mark.anyio
async def test_update_raises_duplicate_error_on_email_conflict(repository):
    customer = create_test_customer()
    other_customer = create_test_customer(email="other@example.com")

    await repository.add_record(customer)
    await repository.add_record(other_customer)

    with pytest.raises(DuplicateItemError, match=f"Customer with email {other_customer.email} already exists."):
        await update_customer(repository, customer.id, UserUpdate(email=other_customer.email))

@pytest.mark.anyio
async def test_create_restaurant_owner_account(repository):
    data = UserCreate(
        email="restaurant_owner@example.com",
        password="password123",
        confirm_password="password123",
        first_name="Alice",
        last_name="Smith"
    )

    result = await create_restaurant_owner(repository, data)

    assert isinstance(result, RestaurantOwner)
    assert result.email == data.email
    assert result.first_name == data.first_name
    assert result.last_name == data.last_name
    assert result.restaurant_id is None  # Since restaurant_id is optional and not provided

    contents = await repository._read_file()

    assert len(contents) == 1

@pytest.mark.anyio
async def test_create_restaurant_owner_raises_duplicate_error(repository):
    existing_owner = create_test_restaurant_owner() 
    await repository.add_record(existing_owner)

    data = UserCreate(
        email=existing_owner.email,
        password="password123",
        confirm_password="password123",
        first_name="Bob",
        last_name="Johnson"
    )

    with pytest.raises(DuplicateItemError, match=f"Restaurant owner with email {existing_owner.email} already exists."):
        await create_restaurant_owner(repository, data)
