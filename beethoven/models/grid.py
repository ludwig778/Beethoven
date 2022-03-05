from __future__ import annotations

from typing import Sequence

from pydantic import BaseModel, Field

from beethoven.models.grid_part import GridPart


class Grid(BaseModel):
    parts: Sequence[GridPart] = Field(default_factory=list)
