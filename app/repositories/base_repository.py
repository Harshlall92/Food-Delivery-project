import json
from pathlib import Path
from types import get_original_bases
from typing import Annotated, Any, Generic, TypeVar, Union, get_args, get_origin

import anyio
from pydantic import BaseModel, TypeAdapter

from app.repositories.exceptions import DuplicateRecordError

T = TypeVar("T", bound=BaseModel)

class BaseRepository(Generic[T]):

    def __init__(self, file_path: str, model: Any) -> None:
        self.file_path = Path(file_path)
        self.model = model
        self.adapter = TypeAdapter(model)

    def _get_concrete_model(self) -> type:
        model_type = None

        orig_class = getattr(self, "__orig_class__", None)
        if orig_class is not None:
            args = get_args(orig_class)
            if args:
                model_type = args[0]

        if model_type is None:
            for base in get_original_bases(type(self)):
                if get_origin(base) is BaseRepository:
                    args = get_args(base)
                    if args:
                        model_type = args[0]
                        break

        if model_type is None:
            return BaseModel

        model_classes = self._extract_actual_classes(model_type)
        return self._find_closest_shared_parent(model_classes)
                            
    def _find_closest_shared_parent(self, classes: list[type]) -> type:
        """Finds the lowest/closest common parent class shared by all listed classes."""
        if not classes:
            return object
        if len(classes) == 1:
            return classes[0]
            
        shared_mro = list(classes[0].__mro__)

        for cls in classes[1:]:
            cls_mro = cls.__mro__
            shared_mro = [c for c in shared_mro if c in cls_mro]
            
        return shared_mro[0] if shared_mro else object 
        
    def _extract_actual_classes(self, t: Any) -> list[type]:
        """Flattens Annotated and Union types into a list of raw classes.""" 
        origin = get_origin(t)
        if origin is Annotated:
            return self._extract_actual_classes(get_args(t)[0])
        if origin is Union:
            classes = []
            for arg in get_args(t):
                classes.extend(self._extract_actual_classes(arg))
            return classes
        if isinstance(t, type):
            return [t]
        return []

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
        record_dict = record.model_dump(by_alias=True)

        if any(item.get("id") == record_dict.get("id") for item in data):
            raise DuplicateRecordError(self._get_concrete_model(), record_dict.get("id")) # type: ignore

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
                data[i] = record.model_dump(by_alias=True)
                await self._write_file(data)
                return self.adapter.validate_python(data[i])
        return None

    async def delete_record(self, record_id: str) -> bool:
        data = await self._read_file()
        for i, item in enumerate(data):
            if item.get("id") == record_id:
                del data[i]
                await self._write_file(data)
                return True
        return False
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