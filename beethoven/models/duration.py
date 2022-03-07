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

    def __add__(self, other: object) -> Duration:
        if not isinstance(other, Duration):
            return NotImplemented

        return Duration(value=self.value + other.value)

    def __iadd__(self, other: object) -> Duration:
        return Duration.__add__(self, other)

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Duration):
            return NotImplemented

        return self.value > other.value
