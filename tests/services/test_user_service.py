import pytest

from app.services.exceptions import UserNotFoundError
from app.schemas.user import Customer, UserCreate, UserUpdate
from app.services.user_service import create_customer, update_customer
from tests.util.helpers import create_user_file, create_user_repository, create_test_customer

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.mark.anyio
async def test_create_customer_account(tmp_path):
    mock_repository = create_user_repository(create_user_file(tmp_path))

    data = UserCreate(
        email="test@example.com",
        password="password123",
        confirm_password="password123",
        first_name="John",
        last_name="Doe"
    )

    result = await create_customer(mock_repository, data)

    assert isinstance(result, Customer)
    assert result.email == data.email
    assert result.first_name == data.first_name
    assert result.last_name == data.last_name

    contents = await mock_repository._read_file()

    assert len(contents) == 1

@pytest.mark.anyio
async def test_update_user_account(tmp_path):
    mock_repository = create_user_repository(create_user_file(tmp_path))
    customer = create_test_customer()
    await mock_repository.add_record(customer)

    customer_id = customer.id

    update_data = UserUpdate(
        email="new_email@test.com",
        password="newpassword",
        confirm_password="newpassword",
        first_name="Tim",
        last_name="Apple",
        active=False
    )

    result = await update_customer(mock_repository, customer_id, update_data)

    assert isinstance(result, Customer)
    assert result.email == update_data.email
    assert result.first_name == update_data.first_name
    assert result.last_name == update_data.last_name
    assert result.active == update_data.active

    updated = await mock_repository.get_by_id(customer_id)

    assert updated is not None
    assert updated["email"] == update_data.email
    assert updated["password"] != customer.password  # Password should be hashed and different
    assert updated["first_name"] == update_data.first_name
    assert updated["last_name"] == update_data.last_name
    assert updated["active"] == update_data.active

@pytest.mark.anyio
async def test_update_raises_user_not_found_error_on_nonexistent_user(tmp_path):
    mock_repository = create_user_repository(create_user_file(tmp_path))

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
        await update_customer(mock_repository, non_existent_id, update_data)