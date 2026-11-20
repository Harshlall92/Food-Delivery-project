import json
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, TypeAdapter
from pathlib import Path
import anyio

T = TypeVar("T", bound=BaseModel)

class BaseRepository(Generic[T]):

    def __init__(self, file_path: str, model: Any) -> None:
        self.file_path = Path(file_path)
        self.model = model
        self.adapter = TypeAdapter(model)

    """
    Database Operations
    """

    async def get_all(self) -> list[T]:
        data = await self._read_file()
        return [
            self.adapter.validate_python(item)
            for item in data
        ]

    async def add_record(self, record: T) -> dict:
        data = await self._read_file()
        record_dict = record.model_dump()

        data.append(record_dict)
        await self._write_file(data)
        return record_dict

    async def get_by_id(self, record_id: str) -> T | None:
        data = await self._read_file()
        for item in data:
            if item.get("id") == record_id:
                return self.adapter.validate_python(item)
        return None

    async def update_record(self, record_id: str, record: T) -> T | None:
        data = await self._read_file()
        for i, item in enumerate(data):
            if item.get("id") == record_id:
                data[i] = record.model_dump()
                await self._write_file(data)
                return self.adapter.validate_python(data[i])
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
