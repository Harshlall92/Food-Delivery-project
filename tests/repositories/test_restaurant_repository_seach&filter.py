import json
import pytest

from tests.util.helpers import create_restaurant_file, create_restaurant_repository

@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def repository(tmp_path):
    restaurant_file = create_restaurant_file(tmp_path)
    restaurant_file.write_text(json.dumps([
        {"id": "1", "name": "kin&folk kelowna", "address": "281 lawrence avenue", "cuisine": "korean", "active": True},
        {"id": "2", "name": "King Tap's", "address": "1352 water street", "cuisine": "continental", "active": True},
    ]))
    return create_restaurant_repository(restaurant_file)


@pytest.mark.anyio
async def test_get_by_name_success(repository):
    result = await repository.get_by_name("King")

    assert [r["id"] for r in result] == ["2"]


@pytest.mark.anyio
async def test_get_by_name_no_match(repository):
    result = await repository.get_by_name("asdasdasdasdasd")

    assert result == []


@pytest.mark.anyio
async def test_get_by_cuisine_success(repository):
    result = await repository.get_by_cuisine("korean")

    assert [r["id"] for r in result] == ["1"]


@pytest.mark.anyio
async def test_get_by_cuisine_no_match(repository):
    result = await repository.get_by_cuisine("mexican")

    assert result == []