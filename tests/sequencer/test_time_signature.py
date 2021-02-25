from pytest import mark, raises

from beethoven.sequencer.note_duration import (Eighths, Half, Quarter,
                                               Septuplet, Sixteenths, Triplet,
                                               Whole)
from beethoven.sequencer.tempo import Tempo
from beethoven.sequencer.time_signature import TimeContainer, TimeSignature


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

    assert repr(time_signature) == f"<Time Signature : {display}>"


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

    assert time_signature.duration(tempo) == duration


@mark.parametrize("time_signature_args,note_duration,num_time,last_time_args", (
    # With whole
    ((4, 4),  Whole, 1, (1, 1, 1)),
    ((3, 4),  Whole, 1, (1, 1, 1)),
    ((3, 8),  Whole, 1, (1, 1, 1)),
    ((5, 16), Whole, 1, (1, 1, 1)),
    ((3, 2),  Whole, 2, (1, 3, 1)),
    # With whole triplets
    ((4, 4),  Triplet(Whole), 3, (1, 3, 3, 3, 3)),
    ((3, 4),  Triplet(Whole), 3, (1, 3, 3, 3, 3)),
    ((3, 8),  Triplet(Whole), 2, (1, 3, 6, 2, 3)),
    ((5, 16), Triplet(Whole), 1, (1, 1, 1, 1, 3)),
    ((3, 2),  Triplet(Whole), 5, (1, 3, 2, 2, 3)),
    # With halfs
    ((4, 4),  Half, 2, (1, 3, 1)),
    ((3, 4),  Half, 2, (1, 3, 1)),
    ((3, 8),  Half, 1, (1, 1, 1)),
    ((5, 16), Half, 1, (1, 1, 1)),
    ((3, 2),  Half, 3, (1, 3, 1)),
    # With halfs triplets
    ((4, 4),  Triplet(Half), 6, (1, 4, 2, 2, 3)),
    ((3, 4),  Triplet(Half), 5, (1, 3, 3, 3, 3)),
    ((3, 8),  Triplet(Half), 3, (1, 3, 6, 2, 3)),
    ((5, 16), Triplet(Half), 2, (1, 3, 11, 3, 3)),
    ((3, 2),  Triplet(Half), 9, (1, 3, 2, 2, 3)),
    # With quarters
    ((4, 4),  Quarter, 4, (1, 4, 1)),
    ((3, 4),  Quarter, 3, (1, 3, 1)),
    ((3, 8),  Quarter, 2, (1, 3, 1)),
    ((5, 16), Quarter, 2, (1, 5, 1)),
    ((3, 2),  Quarter, 6, (1, 3, 2)),
    # With eights
    ((4, 4),  Eighths, 8,  (1, 4, 3, 1, 1)),
    ((3, 4),  Eighths, 6,  (1, 3, 3, 1, 1)),
    ((3, 8),  Eighths, 3,  (1, 3, 1, 1, 1)),
    ((5, 16), Eighths, 3,  (1, 5, 1, 1, 1)),
    ((3, 2),  Eighths, 12, (1, 3, 2, 2, 2)),
    # With sixteenths
    ((4, 4),  Sixteenths, 16, (1, 4, 4, 1, 1)),
    ((3, 4),  Sixteenths, 12, (1, 3, 4, 1, 1)),
    ((3, 8),  Sixteenths, 6,  (1, 3, 5, 1, 1)),
    ((5, 16), Sixteenths, 5,  (1, 5, 1, 1, 1)),
    ((3, 2),  Sixteenths, 24, (1, 3, 2, 4, 4)),
    # With quarter triplets
    ((4, 4),  Triplet(Quarter), 12, (1, 4, 3, 3, 3)),
    ((3, 4),  Triplet(Quarter), 9,  (1, 3, 3, 3, 3)),
    ((3, 8),  Triplet(Quarter), 5,  (1, 3, 6, 2, 3)),
    ((5, 16), Triplet(Quarter), 4,  (1, 5, 1, 1, 3)),
    ((3, 2),  Triplet(Quarter), 18, (1, 3, 2, 3, 3)),
    # With quarter septuplets
    ((4, 4),  Septuplet(Quarter), 28, (1, 4, 4,  4, 7)),
    ((3, 4),  Septuplet(Quarter), 21, (1, 3, 4,  4, 7)),
    ((3, 8),  Septuplet(Quarter), 11, (1, 3, 7,  7, 7)),
    ((5, 16), Septuplet(Quarter), 9,  (1, 5, 10, 2, 7)),
    ((3, 2),  Septuplet(Quarter), 42, (1, 3, 2,  7, 7)),
))
def test_time_signature_generator_run(time_signature_args, note_duration, num_time, last_time_args):
    time_signature = TimeSignature(*time_signature_args)
    time_iterator = list(time_signature.gen(note_duration))

    assert len(time_iterator) == num_time

    assert time_iterator[-1] == TimeContainer(*last_time_args)


def test_time_signature_generator_infinite_loop():
    time_signature = TimeSignature(4, 4)
    gen = time_signature.gen(Whole, go_on=True)

    for _ in range(10):
        time_section = next(gen)

    assert time_section == TimeContainer(10, 1, 1)


def test_time_signature_generator_with_note_range():
    time_signature = TimeSignature(4, 8)
    time_iterator = list(time_signature.gen(Quarter, Whole))

    assert time_iterator[-1] == TimeContainer(2, 3, 1)


def test_time_signature_generator_stop_iteration():
    time_signature = TimeSignature(4, 4)
    gen = time_signature.gen(Whole)

    # Skip the first time_section which is 1/1
    next(gen)

    with raises(StopIteration):
        next(gen)


def test_time_signature_copy():
    time_signature = TimeSignature(3, 4)

    assert time_signature == time_signature.copy()


def test_time_container_equal_method():
    assert TimeContainer(1, 1, 1) == TimeContainer(1, 1, 1, 1, 1)


def test_time_container_comparison_method():
    assert TimeContainer(1, 2, 1) > TimeContainer(1, 1, 1)

    assert TimeContainer(1, 1, 1, 2, 7) > TimeContainer(1, 1, 1, 1, 7)

    assert TimeContainer(1, 1, 1, 1, 7) >= TimeContainer(1, 1, 1, 1, 7)

    assert TimeContainer(1, 1, 1, 5, 7) > TimeContainer(1, 1, 1, 2, 3)

    assert not TimeContainer(1, 1, 2) < TimeContainer(1, 1, 1)

    assert not TimeContainer(1, 2, 1) < TimeContainer(1, 1, 1)


@mark.parametrize("time_signature_args,tempo,note_duration,note_start_offset", (
    ((4, 4),   60, Half,              2.0),
    ((8, 8),   60, Half,              2.0),
    ((16, 16), 60, Half,              2.0),
    ((3, 2),   60, Whole,             4.0),
    ((3, 2),   20, Triplet(Quarter),  1.00),
    ((3, 2),   60, Quarter,           1.0),
    ((15, 16), 60, Sixteenths,        0.25)
))
def test_time_container_start_offset(time_signature_args, tempo, note_duration, note_start_offset):
    time_signature = TimeSignature(*time_signature_args)
    tempo = Tempo(tempo)

    gen = time_signature.gen(note_duration)

    # Skip the first which is equal to 0.0
    next(gen)

    time_section = next(gen)

    assert time_section.start_offset(time_signature, tempo) == note_start_offset


def test_time_container_check():
    time_container = TimeContainer(3, 2, 1, 3, 7)

    assert time_container.check(bar=3)
    assert not time_container.check(bar=2)

    assert time_container.check(bar=(1, 3))
    assert not time_container.check(bar=(1, 2))

    assert time_container.check(bar=3, measure=2)
    assert not time_container.check(bar=3, measure=1)


def test_time_container_copy():
    time_container = TimeContainer(3, 2, 1, 3, 7)

    assert time_container == time_container.copy()


def test_time_container_repr():
    assert repr(TimeContainer(3, 2, 1, 6, 7)) == "<Time 3 | 2 / 1 ( 6 : 7 )>"
