class ServiceError(RuntimeError):
    """Base class for service-related errors."""
    pass

class ItemNotFoundError(ServiceError):
    """Raised when an item is not found in the database."""
    pass

class DuplicateItemError(ServiceError):
    """Raised when attempting to create a duplicate item in the database."""
    pass

class InvalidCredentialsError(ServiceError):
    """Raised when provided credentials are invalid."""
    pass

class CartNotFoundError(ServiceError):
    """Raised when a cart is not found in the database."""
    pass