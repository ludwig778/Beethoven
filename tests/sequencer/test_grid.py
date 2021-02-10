from beethoven.sequencer.grid import Grid
from beethoven.sequencer.tempo import Tempo, default_tempo_factory
from beethoven.sequencer.time_signature import (TimeSignature,
                                                default_time_signature_factory)
from beethoven.theory.chord import Chord
from beethoven.theory.scale import Scale


def test_create_empty_grid():
    grid = Grid()

    assert grid.parts == []

    assert grid.default_tempo == default_tempo_factory()
    assert grid.default_time_signature == default_time_signature_factory()


def test_create_grid_with_parts():
    parts = [
        {"scale": Scale("A", "major"), "chord": Chord("A", "maj")},
        {"chord": Chord("C", "min")},
        {"chord": Chord("E", "maj")},
        {"chord": Chord("G#", "dim")}
    ]
    time_signature = TimeSignature(3, 4)
    tempo = Tempo(90)

    grid = Grid(parts=parts, tempo=tempo, time_signature=time_signature)

    assert len(grid.parts) == 4

    assert grid.default_tempo == tempo
    assert grid.default_time_signature == time_signature

    assert grid.parts[0].tempo == tempo
    assert grid.parts[0].time_signature == time_signature
