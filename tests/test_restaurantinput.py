from pydantic import ValidationError
from app.schemas.restaurant import RestaurantInput


def test_model_creates_with_valid_data():
    data = {
        "name": "Test Restaurant",
        "address": "123 Test St",
        "cuisine": "Italian"
    }

    try:
        restaurant = RestaurantInput(**data)
    except ValidationError:
        assert False, "ValidationError raised unexpectedly"

    assert restaurant.name == "Test Restaurant"

def test_model_raises_validation_error_with_missing_fields():
    data = {
        "name": "Test Restaurant"
    }

    try:
        restaurant = RestaurantInput(**data)
        assert False, "Expected a ValidationError due to missing fields"
    except ValidationError as e:
        assert True
        assert e.error_count() == 2

