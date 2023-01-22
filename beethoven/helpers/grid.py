from copy import deepcopy
from typing import List, Tuple

from beethoven.models import Duration, Grid, TimeSignature
from beethoven.types import GridParts


def get_ordered_grid_parts_by_time_signature(
    grid: Grid,
) -> List[Tuple[TimeSignature, GridParts]]:
    grid_parts_by_time_signature: List[Tuple[TimeSignature, GridParts]] = []

    grid_parts_by_time_signature.append((grid.parts[0].time_signature, [grid.parts[0]]))

    for grid_part in grid.parts[1:]:
        if (
            grid_part.time_signature is None
            or grid_part.time_signature == grid_parts_by_time_signature[-1][0]
        ):
            grid_parts_by_time_signature[-1][1].append(grid_part)
        else:
            grid_parts_by_time_signature.append((grid_part.time_signature, [grid_part]))

    return grid_parts_by_time_signature


def fix_grid_parts_durations(grid: Grid) -> Grid:
    fixed_grid = deepcopy(grid)

    last_time_signature = fixed_grid.parts[0].time_signature
    time_signature_timeline = Duration(value=0)

    for grid_part in fixed_grid.parts:
        if grid_part.time_signature and grid_part.time_signature != last_time_signature:
            last_time_signature = grid_part.time_signature
            time_signature_timeline = Duration(value=0)

        if not grid_part.duration:
            grid_part.duration = last_time_signature.get_duration()

            rest = time_signature_timeline % grid_part.duration

            if rest:
                grid_part.duration -= rest

        time_signature_timeline += grid_part.duration

    return fixed_grid
