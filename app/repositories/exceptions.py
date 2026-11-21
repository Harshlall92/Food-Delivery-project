from typing import Type

from pydantic import BaseModel

class RepositoryError(Exception):
    """Base class for repository-related exceptions."""

    message: str

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class RecordNotFoundError(RepositoryError):
    """Raised when a record is not found in the repository."""

    def __init__(self, model: Type[BaseModel], id: str):
        super().__init__(f"{"Record" if model is BaseModel else model.__name__} with id {id} not found.")

class DuplicateRecordError(RepositoryError):
    """Raised when a duplicate record is added to the repository."""
    id: str

    def __init__(self, model: Type[BaseModel], id: str):
        super().__init__(f"{"Record" if model is BaseModel else model.__name__} with id {id} already exists.")
        self.id = id

class RestaurantNotFoundError(RepositoryError):
    """Raised when a restaurant is not found in the repository."""

    def __init__(self, model: Type[BaseModel], id: str):
        super().__init__(f"{"Restaurant" if model is BaseModel else model.__name__} with id {id} not found.")

class MenuItemNotFoundError(RepositoryError):
    """Raised when a menu item is not found in the repository."""

    def __init__(self, model: Type[BaseModel], id: str):
        super().__init__(f"{"Menu Item" if model is BaseModel else model.__name__} with id {id} not found.")