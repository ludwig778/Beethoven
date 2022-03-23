from copy import deepcopy
from typing import List, Tuple

from beethoven.helpers.time_signature import get_time_signature_duration
from beethoven.models import Grid, TimeSignature
from beethoven.models.duration import Duration
from beethoven.types import GridParts


def get_ordered_grid_parts_by_time_signature(
    grid: Grid,
) -> List[Tuple[TimeSignature, GridParts]]:
    grid_parts_by_time_signature: List[Tuple[TimeSignature, GridParts]] = []

    grid_parts_by_time_signature.append((grid.parts[0].time_signature, [grid.parts[0]]))

    for grid_part in grid.parts[1:]:
        if grid_part.time_signature == grid_parts_by_time_signature[-1][0]:
            grid_parts_by_time_signature[-1][1].append(grid_part)
        else:
            grid_parts_by_time_signature.append((grid_part.time_signature, [grid_part]))

    return grid_parts_by_time_signature


def fix_grid_parts_durations(grid_parts: GridParts) -> GridParts:
    fixed_grid_parts = deepcopy(grid_parts)

    last_time_signature = None

    for grid_part in fixed_grid_parts:
        if grid_part.time_signature != last_time_signature:
            last_time_signature = grid_part.time_signature
            time_signature_timeline = Duration(value=0)

        if not grid_part.duration:
            grid_part.duration = get_time_signature_duration(grid_part.time_signature)

            rest = time_signature_timeline % grid_part.duration

            if rest:
                grid_part.duration -= rest

        time_signature_timeline += grid_part.duration

    return fixed_grid_parts
