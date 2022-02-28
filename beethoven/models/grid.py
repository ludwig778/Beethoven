from __future__ import annotations

from typing import Sequence, Union

from pydantic import BaseModel, Field

from beethoven.models.grid_part import GridPart


class Grid(BaseModel):
    parts: Sequence[Union[Grid, GridPart]] = Field(default_factory=list)
