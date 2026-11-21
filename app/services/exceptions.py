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

class InvalidRoleError(ServiceError):
    """Raised when a user does not have the role required for the operation."""
    pass

class InactiveUserError(ServiceError):
    """Raised when an inactive user attempts an operation."""
    pass

class CustomerNotFoundError(ItemNotFoundError):
    """Raised when a customer is not found."""
    pass

class RestaurantNotFoundError(ItemNotFoundError):
    """Raised when a restaurant is not found."""
    pass

class MenuItemNotFoundError(ItemNotFoundError):
    """Raised when a menu item does not exist."""
    pass

class InactiveMenuItemError(ServiceError):
    """Raised when a menu item is not available and cannot be added to a cart."""
    pass

class InvalidMenuItemError(ServiceError):
    """Raised when a menu item belongs to a different restaurant than the cart."""
    pass

class CartNotFoundError(ServiceError):
    """Raised when a customer does not have an active cart."""
    pass

class DuplicateCartError(DuplicateItemError):
    """Raised when a customer who already has a cart attempts to create another."""
    pass

class OrderNotFoundError(ItemNotFoundError):
    """Raised when an order does not exist."""
    pass

class InvalidOrderStatusError(ServiceError):
    """Raised when an order status is not allowed."""
    pass

class EmptyCartCheckoutError(ServiceError):
    """Raised when checkout is attempted with an empty cart."""
    pass

class CartRestaurantMismatchError(ServiceError):
    """Raised when a cart item or restaurant no longer matches valid cart state."""
    pass