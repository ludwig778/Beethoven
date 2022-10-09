from __future__ import annotations

from pydantic import BaseModel, validator

from beethoven.indexes import degree_index
from beethoven.utils.alterations import get_degree_alteration_str_from_int


class Degree(BaseModel):
    name: str
    alteration: int = 0

    def __str__(self):
        return f"{get_degree_alteration_str_from_int(self.alteration)}{self.name}"

    def __hash__(self):
        return hash(self.name + str(self.alteration))

    @validator("name")
    def name_must_be_valid(cls, name):
        if degree_index.is_valid(name):
            return name

        raise ValueError(f"Invalid name: {name}")

    @validator("alteration")
    def alteration_must_be_valid(cls, alteration):
        if -3 <= alteration <= 3:
            return alteration

        raise ValueError(f"Invalid alteration: {alteration}, must be between -3 and 3")

    @property
    def index(self):
        return degree_index.get_index(self.name)
