from beethoven.sequencer.grid import Grid, GridPart
from beethoven.sequencer.note_duration import Half, Whole
from beethoven.sequencer.tempo import Tempo
from beethoven.sequencer.time_signature import TimeSignature
from beethoven.theory.chord import Chord
from beethoven.theory.scale import Scale


def test_create_empty_grid():
    grid = Grid()

    assert grid.parts == []


def test_create_grid_with_parts():
    parts = [
        {"scale": Scale("A", "major"), "chord": Chord("A", "maj")},
        {"chord": Chord("C", "min"), "tempo": Tempo(120)},
        {"chord": Chord("E", "maj"), "duration": Half},
        {"chord": Chord("G#", "dim"), "time_signature": TimeSignature(3, 2)}
    ]
    time_signature = TimeSignature(4, 4)
    tempo = Tempo(90)

    grid = Grid(
        time_signature=time_signature,
        tempo=tempo,
        duration=Whole
    )
    grid.set_parts(*parts)

    assert repr(grid) == "<Grid : 4 parts>"

    assert len(grid.parts) == 4

    assert grid.parts[0].tempo == tempo
    assert grid.parts[0].time_signature == time_signature


def test_grid_part_repr():
    grid_part = GridPart(
        Scale("C", "ionian"),
        Chord("C", "maj7"),
        Whole,
        TimeSignature(4, 4),
        Tempo(60)
    )

    assert repr(grid_part) == "<GridPart : C ionian / Cmaj7 / Whole / 4/4 / 60>"
