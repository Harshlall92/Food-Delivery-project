import pytest

from tests.util.helpers import create_user_file, create_user_repository, create_test_customer

@pytest.fixture
def anyio_backend():
    return 'asyncio'

@pytest.fixture
def repository(tmp_path):
    user_file = create_user_file(tmp_path)
    user_file.write_text(
        "[\n" +
        create_test_customer().model_dump_json(indent=4) +
        "\n]\n"
    )
    return create_user_repository(user_file)

@pytest.mark.anyio
async def test_contains_email_returns_true_for_existing_email(repository):
    assert await repository.contains_email("test@example.com")

@pytest.mark.anyio
async def test_contains_email_returns_false_for_non_existing_email(repository):
    assert not await repository.contains_email("nonexistent@example.com")