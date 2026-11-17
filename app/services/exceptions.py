class ItemNotFoundError(RuntimeError):
    """Raised when an item is not found in the database."""
    pass

class UserNotFoundError(ItemNotFoundError):
    """Raised when a user is not found in the database."""
    pass

class DuplicateItemError(RuntimeError):
    """Raised when attempting to create a duplicate item in the database."""
    pass