import json

from pydantic import BaseModel
from pathlib import Path
import anyio

class BaseRepository[T: BaseModel]:

    file_path: Path

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    """
    Database Operations
    """

    async def get_all(self) -> list[dict]:
        return await self._read_file()

    async def add_record(self, record: T) -> dict:
        data = await self._read_file()
        record_dict = record.model_dump()

        data.append(record_dict)
        await self._write_file(data)
        return record_dict

    async def get_by_id(self, record_id: str) -> dict | None:
        data = await self._read_file()
        for item in data:
            if item.get("id") == record_id:
                return item
        return None

    """
    Data Persistence Methods
    """

    async def _read_file(self) -> list[dict]:
        try:
            async with await anyio.open_file(self.file_path, "r", encoding="utf-8") as file:
                contents = await file.read()
                return json.loads(contents)
        except FileNotFoundError:
            await self._handle_file_not_found()
        except json.JSONDecodeError:
            await self._handle_invalid_json()
        return []

    async def _write_file(self, data: list[dict]):
        async with await anyio.open_file(self.file_path, "w", encoding="utf-8") as file:
            await file.write(json.dumps(data, indent=4))

    """
    Error Handling
    """

    async def _handle_file_not_found(self):
        async with await anyio.open_file(self.file_path, "w", encoding="utf-8") as file:
            await file.write("[]")

    async def _handle_invalid_json(self):
        async with await anyio.open_file(self.file_path, "w", encoding="utf-8") as file:
            await file.write("[]")
