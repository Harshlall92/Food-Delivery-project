import bcrypt
import re
from uuid6 import uuid7
from typing_extensions import Annotated, Literal, Union, Self
from pydantic import BaseModel, Field, field_validator, model_validator

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid7()), frozen=True)
    email: str
    password: str
    first_name: str
    last_name: str
    active: bool = Field(default=True)

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, value):
        value = value.strip()
        if not re.match(r"[\w]+@[\w]+\.[\w]+", value):
            raise ValueError("Invalid email address")
        return value.lower()

    @field_validator("first_name", "last_name", mode="before")
    @classmethod
    def validate_names(cls, value):
        value = value.strip()
        if value == "":
            raise ValueError("Name fields cannot be empty")
        return value.title()

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, value):
        value = value.strip()
        if value == "":
            raise ValueError("Password cannot be empty")
        if bool(re.search(r"[\s]", value)):
            raise ValueError("Password cannot contain whitespace")
        
        return bcrypt.hashpw(value.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

class Address(BaseModel):
    street_address: str = Field(min_length=1)
    city: str = Field(min_length=1)
    province: str = Field(min_length=1)
    postal_code: str = Field(min_length=1)
    label: str = Field(min_length=1) 

class Customer(User):
    role: Literal["customer"] = "customer"
    addresses: list[Address] = Field(default_factory=list)
    payment_method: str | None = Field(default=None, min_length=1)  # Unused for now

class RestaurantOwner(User):
    role: Literal["restaurant_owner"] = "restaurant_owner"
    restaurant_id: str | None = Field(default=None) # Account is created before restaurant is created, so this field is optional

class Admin(User):
    role: Literal["admin"] = "admin"
    permissions: list[str] = Field(default_factory=list) # Unused for now

AnyUser = Annotated[Union[Customer, RestaurantOwner, Admin], Field(discriminator="role")]

class UserUpdate(BaseModel):
    email: str | None = Field(default=None)
    password: str | None = Field(default=None)
    confirm_password: str | None = Field(default=None)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    active: bool | None = Field(default=None)

    @model_validator(mode="after")
    def validate_passwords_match(self) -> Self:
        if self.password is not None and self.confirm_password is None:
            raise ValueError("confirm_password is required when password is provided")
        if self.password is not None and self.confirm_password is not None:
            if self.password != self.confirm_password:
                raise ValueError("password and confirm_password do not match")
        return self

class UserCreate(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)
    confirm_password: str = Field(min_length=1)
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_passwords_match(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match.")
        return self
