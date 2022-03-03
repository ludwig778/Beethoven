from __future__ import annotations

from pydantic import BaseModel, validator

from beethoven.indexes import interval_index
from beethoven.utils.alterations import get_interval_alteration_str_from_int


class Interval(BaseModel):
    name: str
    alteration: int = 0

    @validator("name")
    def name_must_be_valid(cls, name):
        if interval_index.is_valid(name):
            return name

        raise ValueError(f"Invalid name: {name}")

    @validator("alteration")
    def alteration_must_be_valid(cls, alteration):
        if -3 <= alteration <= 3:
            return alteration

        raise ValueError(f"Invalid alteration: {alteration}, must be between -3 and 3")

    def __str__(self):
        alteration_str = get_interval_alteration_str_from_int(
            self.alteration, int(self.name)
        )

        return f"{self.name}{alteration_str}"
