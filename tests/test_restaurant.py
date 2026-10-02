import pytest
from pydantic import ValidationError
from app.schemas.restaurant import Restaurant

def test_restaurant_valid_creation():
    r=Restaurant(name= "Test", address="street", cuisine="italian")
    assert isinstance(r.id,str)
    assert r.active is True

def test_restaurant_missing_name():
    with pytest.raises(ValidationError):
        Restaurant(address= "street", cuisine = "italian")

def test_restaurant_missing_address():
    with pytest.raises(ValidationError):
            Restaurant(name= "test", cuisine = "italian")

def test_restaurant_missing_cuisine():
    with pytest.raises(ValidationError):
            Restaurant(name= "Test", address = "street")

def test_restaurant_active_defaults_true():
    r=Restaurant(name= "Test", address="street", cuisine="italian")
    assert r.active is True

def test_restaurant_unique_id():
    r = Restaurant(name = "test1", address="street1", cuisine= "thai")
    s = Restaurant(name = "test2", address="street2", cuisine= "mexican")
    assert r.id != s.id

def test_restaurant_idfreeze():
     r = Restaurant(name="Test", address="123 Main St", cuisine="italian")
     with pytest.raises(ValidationError):
          r.id = "diff-id"

