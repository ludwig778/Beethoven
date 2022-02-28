from __future__ import annotations

from pydantic import BaseModel, validator


class Bpm(BaseModel):
    value: int

    @validator("value")
    def value_must_be_within_range(cls, value):
        if 0 < value <= 600:
            return value

        raise ValueError(f"Invalid value: {value}, must be between 0 and 600")
