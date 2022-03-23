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

    def __hash__(self):
        return hash(self.value)

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

    def __ge__(self, other: object) -> bool:
        return self.value == other.value or self.value > other.value

    def __mul__(self, other: object) -> Duration:
        return Duration(value=self.value * other)

    def __sub__(self, other: object) -> Duration:
        return Duration(value=self.value - other.value)

    def __mod__(self, other) -> Duration:
        return Duration(value=self.value % other.value)

    def __floordiv__(self, other) -> Duration:
        return Duration(value=self.value // other.value)
