from __future__ import annotations

from fractions import Fraction

from pydantic import BaseModel, validator


class Duration(BaseModel):
    value: Fraction

    @validator("value", pre=True)
    def cast_int_to_fraction(cls, value):
        if isinstance(value, int):
            value = Fraction(value)

        return value

    class Config:
        arbitrary_types_allowed = True
