from __future__ import annotations

from pydantic import BaseModel, validator


class TimeSignature(BaseModel):
    beats_per_bar: int
    beat_unit: int

    @validator("beat_unit")
    def beat_unit_must_be_within_range(cls, beat_unit):
        if 1 <= beat_unit <= 32:
            return beat_unit

        raise ValueError(f"Invalid beat_unit: {beat_unit}, must be in range 1-32")

    @validator("beat_unit")
    def beat_unit_must_be_a_multiple_of_2(cls, beat_unit):
        if beat_unit in (1, 2, 4, 8, 16, 32):
            return beat_unit

        raise ValueError(f"Invalid beat_unit: {beat_unit}, must be a multiple of 2")
