from decimal import Decimal

from pydantic import BaseModel, Field, PlainSerializer, field_validator, PositiveInt
from typing_extensions import Annotated, Literal

CanadianProvinceCode = Literal[
    "AB", "BC", "MB", "NB", "NL", "NS", "NT",
    "NU", "ON", "PE", "QC", "SK", "YT"
]

class BaseAddress(BaseModel):
    address_line_1: str = Field(min_length=1, max_length=120)
    address_line_2: str | None = Field(default=None, min_length=1, max_length=120)
    city: str = Field(min_length=1, max_length=50)
    province: CanadianProvinceCode
    country: Literal["Canada"] = "Canada"
    postal_code: str = Field(pattern=r"^[A-Z]\d[A-Z] \d[A-Z]\d$")

    @field_validator("address_line_1", "address_line_2", "city", mode="before")
    @classmethod
    def validate_non_empty(cls, value):
        if value is not None:
            value = value.strip()
            if value == "":
                raise ValueError("Field cannot be empty")
        return value

Price = Annotated[
            Decimal,
            Field(ge=0, decimal_places=2, max_digits=10, examples=["9.99"]),
            PlainSerializer(lambda x: str(x), return_type=str)
        ]

CartQuantity = PositiveInt