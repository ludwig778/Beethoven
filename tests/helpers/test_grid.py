from beethoven.helpers.grid import get_ordered_grid_parts_by_time_signature
from beethoven.models import Bpm, Grid, GridPart, TimeSignature
from tests.fixtures.chords import c_maj7, d_min7, e_min7, g_7
from tests.fixtures.scales import a_minor, c_major


def test_grid_helper_get_ordered_grid_parts_by_time_signature():
    bpm = Bpm(value=120)
    time_signatures = [
        TimeSignature(beats_per_bar=4, beat_unit=4),
        TimeSignature(beats_per_bar=3, beat_unit=2),
        TimeSignature(beats_per_bar=5, beat_unit=8),
    ]

    grid = Grid(
        parts=[
            GridPart(
                scale=c_major,
                chord=d_min7,
                bpm=bpm,
                time_signature=time_signatures[0],
                duration=None,
            ),
            GridPart(
                scale=c_major,
                chord=g_7,
                bpm=bpm,
                time_signature=time_signatures[1],
                duration=None,
            ),
            GridPart(
                scale=a_minor,
                chord=e_min7,
                bpm=bpm,
                time_signature=time_signatures[1],
                duration=None,
            ),
            GridPart(
                scale=a_minor,
                chord=c_maj7,
                bpm=bpm,
                time_signature=time_signatures[2],
                duration=None,
            ),
        ]
    )

    grid_parts_by_time_signature = get_ordered_grid_parts_by_time_signature(grid)

    assert grid_parts_by_time_signature == [
        (time_signatures[0], grid.parts[:1]),
        (time_signatures[1], grid.parts[1:3]),
        (time_signatures[2], grid.parts[3:]),
    ]
