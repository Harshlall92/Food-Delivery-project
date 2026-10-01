import json

from pydantic import BaseModel
from pathlib import Path
from anyio import open_file

class BaseRepository[T: BaseModel]:

    file_path: Path

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    """
    Database Operations
    """

    async def get_all(self) -> list[dict]:
        return await self._read_file()

    async def add_record(self, record: T):
        data = await self._read_file()
        data.append(record.model_dump())
        await self._write_file(data)

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
            async with await open_file(self.file_path, "r", encoding="utf-8") as file:
                contents = await file.read()
                return json.loads(contents)
        except FileNotFoundError:
            await self._handle_file_not_found()
        except json.JSONDecodeError:
            await self._handle_invalid_json()
        return []

    async def _write_file(self, data: list[dict]):
        async with await open_file(self.file_path, "w", encoding="utf-8") as file:
            await file.write(json.dumps(data, indent=4))

    """
    Error Handling
    """

    async def _handle_file_not_found(self):
        async with await open_file(self.file_path, "w", encoding="utf-8") as file:
            await file.write("[]")

    async def _handle_invalid_json(self):
        async with await open_file(self.file_path, "w", encoding="utf-8") as file:
            await file.write("[]")
