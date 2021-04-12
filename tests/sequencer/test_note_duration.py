from pytest import mark

# from beethoven.sequencer.state import default_tempo
from beethoven.sequencer.note_duration import (Eighths, Half, Nontuplet,
                                               Quarter, Septuplet, Sixteenths,
                                               Triplet, Whole)
from beethoven.sequencer.tempo import Tempo


@mark.parametrize("note_duration,multiplier_to_whole", (
    (Whole,              1),
    (Half,               2),
    (Quarter,            4),
    (Eighths,            8),
    (Triplet(Half),      2 * 3),
    (Triplet(Quarter),   4 * 3),
    (Nontuplet(Quarter), 4 * 9)
))
def test_note_duration_comparison_objects(note_duration, multiplier_to_whole):
    assert (note_duration * multiplier_to_whole) == Whole


@mark.parametrize("note_duration,display", (
    (Whole, "Whole"),
    (Half, "Half"),
    (Quarter, "Quarter"),
    (Eighths, "Eighths"),
    (Sixteenths, "Sixteenths"),
    (Triplet(Quarter), "Quarter Triplet"),
    (Septuplet(Quarter), "Quarter Septuplet")
))
def test_note_duration_representation(note_duration, display):
    assert repr(note_duration) == f"<Note Duration : {display}>"


@mark.parametrize("note_duration", (Whole, Half, Quarter, Eighths))
def test_note_duration_with_different_tempos(note_duration):
    assert note_duration.duration(bpm=Tempo(50)) != note_duration.duration(bpm=Tempo(40))
