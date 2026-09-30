import json
import pytest
from app.repositories.base_repository import BaseRepository

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.mark.anyio
async def test_repository_can_read_file(tmp_path):
    file_path = tmp_path / "test.json"
    data = [{"id": 1, "name": "Test"}]
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

