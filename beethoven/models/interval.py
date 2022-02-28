from __future__ import annotations

from pydantic import BaseModel, validator

from beethoven.indexes import interval_index


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
