import pytest

from app.schemas.user import Customer, UserCreate
from app.services.user_service import create_customer
from tests.util.helpers import create_user_file, create_user_repository

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