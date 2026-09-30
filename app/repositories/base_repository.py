import json

from typing import TypeVar, Generic
from pydantic import BaseModel
from pathlib import Path
from anyio import open_file



class BaseRepository:

    file_path: Path
    T = TypeVar('T', bound=BaseModel)

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

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
