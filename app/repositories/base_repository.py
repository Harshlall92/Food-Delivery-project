import json

from typing import TypeVar, Generic
from pydantic import BaseModel
from pathlib import Path
from anyio import open_file



class BaseRepository:

    filepath: Path
    T = TypeVar('T', bound=BaseModel)

    def __init__(self, file_path: str):
        self.filepath = Path(file_path)

    async def _read_file(self) -> list[dict]:
        try:
            async with await open_file(self.filepath, "r", encoding="utf-8") as file:
                contents = await file.read()
                return json.loads(contents)
        except FileNotFoundError:
            await self._handle_file_not_found()
        except json.JSONDecodeError:
            await self._handle_invalid_json()
        return []

    async def _handle_file_not_found(self):
        async with await open_file(self.filepath, "w", encoding="utf-8") as file:
            await file.write("[]")

    async def _handle_invalid_json(self):
        async with await open_file(self.filepath, "w", encoding="utf-8") as file:
            await file.write("[]")
