import json
import pytest
from app.repositories.base_repository import BaseRepository

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.mark.anyio
async def test_repository_can_read_file(tmp_path):
    assert False

@pytest.mark.anyio
async def test_repository_handles_file_not_found_on_read(tmp_path):
    assert False

@pytest.mark.anyio
async def test_repository_handles_invalid_json_on_read(tmp_path):
    assert False
