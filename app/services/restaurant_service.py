from app.repositories.restaurant_repository import RestaurantRepository
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.exceptions import RecordNotFoundError
from app.services import menu_item_service as mService
from app.services.exceptions import ItemNotFoundError
from app.schemas.restaurant import *


async def get_restaurants(repository: RestaurantRepository) -> list[Restaurant]:
    return await repository.get_all()

async def get_restaurants_by_name(repository: RestaurantRepository, name: str) -> list[Restaurant]:

    query = await repository.get_by_name(name)

    if not query:
        raise ItemNotFoundError(f"No restaurants found matching {name}.")
    
    return query


async def get_restaurants_by_cuisine(repository: RestaurantRepository, cuisine: str) -> list[Restaurant]:
    query = await repository.get_by_cuisine(cuisine)

    if not query:
        raise ItemNotFoundError(f"Restaurant with cuisine {cuisine} not found.")
        
    return query

async def get_all_cuisines(repository: RestaurantRepository) -> list:
    return []


async def create_restaurants(repository: RestaurantRepository, data: RestaurantInput) -> Restaurant:
    record = Restaurant(**data.model_dump())

    await repository.add_record(record)

    return record


async def get_full_restaurant_info(restaurant_repository: RestaurantRepository, menu_item_repository: MenuItemRepository, restaurant_id: str) -> FullRestaurantOutput | None:

    try:
        restaurant = await restaurant_repository.get_by_id(restaurant_id)
    except RecordNotFoundError as e:
        raise ItemNotFoundError(e.message)

    menu_items = await mService.get_menu_items_by_restaurant_id(menu_item_repository, restaurant_id)

    return FullRestaurantOutput(
        **restaurant.model_dump(),
        menu_items=menu_items
    )
async def update_restaurant(restaurant_repository: RestaurantRepository, restaurant_id: str, payload: RestaurantUpdate) -> Restaurant:
    try:
        restaurant = await restaurant_repository.get_by_id(restaurant_id)
    except RecordNotFoundError as e:
        raise ItemNotFoundError(e.message)

    changes = payload.model_dump(exclude_unset=True)
    updated = Restaurant(**{**restaurant.model_dump(), **changes})
    result = await restaurant_repository.update_record(restaurant_id, updated)
    if result is None:
        raise mService.RestaurantNotFoundError(restaurant_id)
    return result

def validate_restaurant(restaurant: dict) -> Restaurant:
    return Restaurant(**restaurant)
