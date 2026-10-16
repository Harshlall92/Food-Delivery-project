from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.menu_item import MenuItem, MenuItemInput, MenuItemOutput


class RestaurantNotFoundError(Exception):
    """Raised when a menu item is added to a restaurant that doesn't exist."""


async def create_menu_item(
    restaurant_repository: RestaurantRepository,
    menu_item_repository: MenuItemRepository,
    restaurant_id: str,
    data: MenuItemInput,
) -> MenuItem:
    """make sure not to add menu items to restraunts that dont exist"""
    restaurant = await restaurant_repository.get_by_id(restaurant_id)
    if restaurant is None:
        raise RestaurantNotFoundError(f"Restaurant {restaurant_id} not found")

    record = MenuItem(restaurant_id=restaurant_id, **data.model_dump())
    await menu_item_repository.add_record(record)
    return record

async def get_menu_items_by_restaurant_id(menu_item_repository: MenuItemRepository, restaurant_id: str) -> list[MenuItemOutput]:
    menu_items = await menu_item_repository.get_menu_items_by_restaurant_id(restaurant_id)
    return [validate_menu_item(item) for item in menu_items]

def validate_menu_item(menu_item: dict) -> MenuItemOutput:
    return MenuItemOutput(**menu_item)

#check