from pytest import mark

from beethoven.sequencer.tempo import Tempo
from beethoven.sequencer.note_duration import (Eighths, Half, Quarter, Quintuplet,
                                               Septuplet, Sixteenths, Triplet,
                                               Whole)
from beethoven.sequencer.time_signature import TimeContainer, TimeSignature

"""

@mark.parametrize("args,display", (
    ((),      "4/4"),
    ((4, 4),  "4/4"),
    ((3, 8),  "3/8"),
    ((9, 8),  "9/8"),
    ((5, 16), "5/16"),
    ((3, 2),  "3/2")
))
def test_time_signature_instanciation(args, display):
    time_signature = TimeSignature(*args)

    assert str(time_signature) == f"<Time Signature : {display}>"


@mark.parametrize("args,tempo,duration", (
    ((),       80,  3.0),
    ((2, 2),   60,  4.0),
    ((4, 4),   60,  4.0),
    ((8, 8),   60,  4.0),
    ((16, 16), 60,  4.0),
    ((3, 8),   120, 0.75),
    ((9, 8),   60,  4.5),
    ((5, 16),  100, 0.75),
    ((3, 2),   20,  18.0)
))
def test_time_signature_duration(args, tempo, duration):
    time_signature = TimeSignature(*args)
    tempo = Tempo(tempo)

    assert time_signature.get_duration(tempo) == duration
"""

@mark.parametrize("time_signature_args,note_duration,num_time,last_time_args", (
    # With whole
    #((4, 4),  Whole, 1, (1, 1)),
    #((3, 4),  Whole, 1, (1, 1)),
    #((3, 8),  Whole, 1, (1, 1)),
    #((5, 16), Whole, 1, (1, 1)),
    #((3, 2),  Whole, 2, (3, 1)),
    # With whole triplets
    #((4, 4),  Triplet(Whole), 3, (3, 3, 3, 3)),
    #((3, 4),  Triplet(Whole), 3, (3, 3, 3, 3)),
    #((3, 8),  Triplet(Whole), 2, (3, 6, 2, 3)),
    #((5, 16), Triplet(Whole), 1, (1, 1, 1, 3)),
    #((3, 2),  Triplet(Whole), 5, (3, 2, 2, 3)),
    # With halfs
    #((4, 4),  Half, 2, (3, 1)),
    #((3, 4),  Half, 2, (3, 1)),
    #((3, 8),  Half, 1, (1, 1)),
    #((5, 16), Half, 1, (1, 1)),
    #((3, 2),  Half, 3, (3, 1)),
    # With quarters
    #((4, 4),  Quarter, 4, (4, 1)),
    #((3, 4),  Quarter, 3, (3, 1)),
    #((3, 8),  Quarter, 2, (3, 1)),
    #((5, 16), Quarter, 2, (5, 1)),
    #((3, 2),  Quarter, 6, (3, 2)),
    # With eights
    ((4, 4),  Eighths, 8,  (4, 3, 1, 2)),
    ((3, 4),  Eighths, 6,  (3, 3, 1, 2)),
    ((3, 8),  Eighths, 3,  (3, 1, 1, 2)),
    ((5, 16), Eighths, 3,  (5, 1, 1, 2)),
    ((3, 2),  Eighths, 12, (3, 2, 2, 2)),
    # With sixteenths
    ((4, 4),  Sixteenths, 16, (4, 4, 1, 4)),
    ((3, 4),  Sixteenths, 12, (3, 4, 1, 4)),
    ((3, 8),  Sixteenths, 6,  (3, 5, 1, 4)),
    ((5, 16), Sixteenths, 5,  (5, 1, 1, 4)),
    ((3, 2),  Sixteenths, 24, (3, 2, 4, 4)),
    # With quarter triplets
    #((4, 4),  Triplet(Quarter), 12, (4, 3, 3, 3)),
    #((3, 4),  Triplet(Quarter), 9,  (3, 3, 3, 3)),
    #((3, 8),  Triplet(Quarter), 5,  (3, 6, 2, 3)),
    #((5, 16), Triplet(Quarter), 4,  (5, 1, 1, 3)),
    #((3, 2),  Triplet(Quarter), 18, (3, 2, 3, 3)),
    # With quarter septuplets
    #((4, 4),  Septuplet(Quarter), 28, (4, 4,  4, 7)),
    #((3, 4),  Septuplet(Quarter), 21, (3, 4,  4, 7)),
    #((3, 8),  Septuplet(Quarter), 11, (3, 7,  7, 7)),
    #((5, 16), Septuplet(Quarter), 9,  (5, 10, 2, 7)),
    #((3, 2),  Septuplet(Quarter), 42, (3, 2,  7, 7)),
))
def test_time_signature_generator_run(time_signature_args, note_duration, num_time, last_time_args):
    time_signature = TimeSignature(*time_signature_args)
    print()
    time_iterator = list(time_signature.gen(note_duration))
    from pprint import pprint as pp
    print(time_signature, note_duration)
    pp(time_iterator)

    assert len(time_iterator) == num_time

    assert time_iterator[-1] == TimeContainer(*last_time_args)

"""

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
    assert str(note_duration) == f"<Note Duration : {display}>"

@mark.parametrize("time_signature_args,note_duration", (
    #((2, 4),  Whole),
    #((2, 4),  Half),
    #((2, 2),  Half),
    #((2, 4),  Quarter),
    #((2, 2),  Quarter),
    #((2, 4),  Eighths),
    #((4, 8),  Eighths),
    ((4, 4),  Quintuplet(Whole)),
    ((4, 4),  Quintuplet(Half)),
    ((4, 4),  Quintuplet(Quarter)),
    ((4, 4),  Triplet(Quarter)),
    ((4, 4),  Sixteenths),
    ((5, 8),  Quarter),
    ((2, 2),  Quarter),
    ((5, 16), Quarter)
))
def test_note_duration_(time_signature_args, note_duration):
    time_signature = TimeSignature(*time_signature_args)
    from pprint import pprint as pp
    print()
    gen = list(time_signature.gen(note_duration))
    pp(gen)
    print()
    #print(gen[0])
    #print(gen[1])
    #print(gen[2])
    #pp(gen)


def test_time_container_equal_method():
    assert TimeContainer(1, 1) == TimeContainer(1, 1, 1, 1)


def test_time_container_greater_than_method():
    assert TimeContainer(2, 1) > TimeContainer(1, 1)

    assert TimeContainer(1, 1, 2, 7) > TimeContainer(1, 1, 1, 7)

    assert TimeContainer(1, 1, 5, 7) > TimeContainer(1, 1, 2, 3)
"""
