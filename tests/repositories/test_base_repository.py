import json
import pytest
from app.repositories.base_repository import BaseRepository
from tests.schemas import TestModel

@pytest.fixture
def anyio_backend():
    return "asyncio"

"""
Reading From File Tests
"""

@pytest.mark.anyio
async def test_repository_can_read_file(tmp_path):
    file_path = tmp_path / "test.json"
    data = [{"id": "1", "name": "Test"}]
    file_path.write_text(json.dumps(data), encoding="utf-8")

    repository = BaseRepository(file_path=str(file_path))

    content = await repository._read_file()

    assert content == data

@pytest.mark.anyio
async def test_repository_handles_file_not_found_on_read(tmp_path):
    file_path = tmp_path / "non_existent.json"

    repository = BaseRepository(file_path=str(file_path))

    assert not file_path.exists()

    content = await repository._read_file()

    assert content == []
    assert file_path.exists()
    assert file_path.read_text(encoding="utf-8") == "[]"

@pytest.mark.anyio
async def test_repository_handles_invalid_json_on_read(tmp_path):
    file_path = tmp_path / "invalid.json"
    file_path.write_text("not valid json", encoding="utf-8")

    repository = BaseRepository(file_path=str(file_path))

    content = await repository._read_file()

    assert content == []
    assert file_path.exists()
    assert file_path.read_text(encoding="utf-8") == "[]"

"""
Writing To File Tests
"""

@pytest.mark.anyio
async def test_repository_can_write_to_file(tmp_path):
    file_path = tmp_path / "test_write.json"
    data = [{"id": "1", "name": "Test"}]

    file_path.write_text("", encoding="utf-8")

    repository = BaseRepository(file_path=str(file_path))

    assert file_path.exists() == True

    await repository._write_file(data)

    content = json.loads(file_path.read_text(encoding="utf-8"))

    assert content == data

    """
    Database Operations Tests
    """

@pytest.mark.anyio
async def test_repository_can_get_all_items(tmp_path):
    file_path = tmp_path / "test.json"
    data = [{"id": "1", "name": "Test"}]
    file_path.write_text(json.dumps(data), encoding="utf-8")

    repository = BaseRepository(file_path=str(file_path))

    items = await repository.get_all()

    assert items == data

@pytest.mark.anyio
async def test_repository_returns_empty_list_if_file_is_empty(tmp_path):
    file_path = tmp_path / "empty.json"
    file_path.write_text("", encoding="utf-8")

    repository = BaseRepository(file_path=str(file_path))

    items = await repository.get_all()

    assert items == []

@pytest.mark.anyio
async def test_repository_can_add_item_to_database(tmp_path):
    file_path = tmp_path / "test.json"
    data = [{"id": "1", "name": "Test"}]
    file_path.write_text(json.dumps(data), encoding="utf-8")

    repository = BaseRepository(file_path=str(file_path))

    new_item = TestModel(id="2", name="Another Item")
    await repository.add_record(new_item)

    content = json.loads(file_path.read_text(encoding="utf-8"))

    assert len(content) == 2

@pytest.mark.anyio
async def test_repository_can_add_item_to_non_existent_database(tmp_path):
    file_path = tmp_path / "test.json"

    repository = BaseRepository(file_path=str(file_path))

    new_item = TestModel(id="1", name="New Item")
    await repository.add_record(new_item)

    content = json.loads(file_path.read_text(encoding="utf-8"))

    assert len(content) == 1

@pytest.mark.anyio
async def test_repository_can_get_item_by_id(tmp_path):
    file_path = tmp_path / "test.json"
    data = [{"id": "1", "name": "Test"}, {"id": "2", "name": "Another Test"}]
    file_path.write_text(json.dumps(data), encoding="utf-8")

    repository = BaseRepository(file_path=str(file_path))

    item = await repository.get_by_id("2")

    assert item == {"id": "2", "name": "Another Test"}

@pytest.mark.anyio
async def test_repository_returns_none_if_item_not_found(tmp_path):
    file_path = tmp_path / "test.json"
    data = [{"id": "1", "name": "Test"}]
    file_path.write_text(json.dumps(data), encoding="utf-8")

    repository = BaseRepository(file_path=str(file_path))

    item = await repository.get_by_id("2")

    assert item is None