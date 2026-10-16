from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.menu_item_repository import MenuItemRepository
from app.services import menu_item_service as mService
from app.schemas.restaurant import *


async def get_restaurants(repository: RestaurantRepository) -> list[Restaurant]:

    query = await repository.get_all()

    return [
        validate_restaurant(restaurant)
        for restaurant in query
    ]

async def create_restaurants(repository: RestaurantRepository, data: RestaurantInput) -> Restaurant:
    record = Restaurant(**data.model_dump())

    await repository.add_record(record)

    return record


async def get_full_restaurant_info(restaurant_repository: RestaurantRepository, menu_item_repository: MenuItemRepository, restaurant_id: str) -> FullRestaurantOutput | None:

    restaurant = await restaurant_repository.get_by_id(restaurant_id)

    if restaurant is None:
        raise mService.RestaurantNotFoundError(f"Restaurant with ID {restaurant_id} not found.")

    menu_items = await mService.get_menu_items_by_restaurant_id(menu_item_repository, restaurant_id)

    return FullRestaurantOutput(
        **restaurant,
        menu_items=menu_items
    )
async def update_restaurant(restaurant_repository: RestaurantRepository, restaurant_id: str, payload: RestaurantUpdate) -> Restaurant:
    restaurant = await restaurant_repository.get_by_id(restaurant_id)
    if restaurant is None:
        raise mService.RestaurantNotFoundError(restaurant_id)
    changes = payload.model_dump(exclude_unset=True)
    updated = Restaurant(**{**restaurant, **changes})
    result = await restaurant_repository.update_record(restaurant_id, updated)
    return validate_restaurant(result)

def validate_restaurant(restaurant: dict) -> Restaurant:
    return Restaurant(**restaurant)
