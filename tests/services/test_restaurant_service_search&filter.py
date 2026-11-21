import pytest
from unittest.mock import AsyncMock

from app.schemas.restaurant import Restaurant
from app.services.exceptions import ItemNotFoundError
from app.services.restaurant_service import get_restaurants_by_name, get_restaurants_by_cuisine
from tests.util.helpers import create_restaurant_file, create_restaurant_repository


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def repository(tmp_path):
    return create_restaurant_repository(create_restaurant_file(tmp_path))


TEST_RESTAURANT = [
    {"id": "01a0fd78-2c5c-72f4-b913-672a802a7116", "name": "kin&folk kelowna", "address": "281 lawrence avenue", "cuisine": "korean"},
]


@pytest.mark.anyio
async def test_get_restaurants_by_name_success(repository):
    await repository._write_file(TEST_RESTAURANT)

    result = await get_restaurants_by_name(repository, "kin")

    assert len(result) == 1
    assert isinstance(result[0], Restaurant)
    assert result[0].name == "kin&folk kelowna"


@pytest.mark.anyio
async def test_get_restaurants_by_name_not_found(repository):
    with pytest.raises(ItemNotFoundError):
        await get_restaurants_by_name(repository, "asdasdasdasdasd")


@pytest.mark.anyio
async def test_get_restaurants_by_cuisine_success(repository):
    await repository._write_file(TEST_RESTAURANT)

    result = await get_restaurants_by_cuisine(repository, "korean")

    assert len(result) == 1
    assert isinstance(result[0], Restaurant)
    assert result[0].cuisine == "korean"


@pytest.mark.anyio
async def test_get_restaurants_by_cuisine_not_found(repository):
    with pytest.raises(ItemNotFoundError):
        await get_restaurants_by_cuisine(repository, "mexican")
