from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.restaurant import Restaurant

async def get_restaurants() -> list[Restaurant]:
    """
    Fetches a list of restaurants from the restaurant repository.
    
    Returns:
        list: A list of restaurant objects.
    """
    repo = RestaurantRepository()

    query = await repo.get_restaurants()

    return [
        validate_restaurant(restaurant)
        for restaurant in query
    ]

def validate_restaurant(restaurant: dict) -> Restaurant:
    """
    Validates and converts a restaurant dictionary to a Restaurant object.
    
    Args:
        restaurant (dict): A dictionary representing a restaurant.
    
    Returns:
        Restaurant: A validated Restaurant object.
    """

    if restaurant["name"] is None:
        raise ValueError("Restaurant name cannot be None")
    if restaurant["address"] is None:
        raise ValueError("Restaurant address cannot be None")
    if restaurant["cuisine"] is None:
        raise ValueError("Restaurant cuisine cannot be None")

    return Restaurant(
        id=restaurant["id"],
        name=restaurant["name"],
        address=restaurant["address"],
        cuisine=restaurant["cuisine"]
    )

