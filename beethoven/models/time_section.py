from __future__ import annotations

from fractions import Fraction

from pydantic import BaseModel, validator


class TimeSection(BaseModel):
    bar: int
    measure: int
    rest: Fraction

    @validator("rest", pre=True)
    def cast_int_to_fraction(cls, rest):
        if isinstance(rest, int):
            rest = Fraction(rest)

        return rest

    class Config:
        arbitrary_types_allowed = True
