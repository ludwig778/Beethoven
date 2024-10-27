from pytest import fixture, raises

from beethoven.models import (Bpm, Chord, ChordItem, Degree, Duration,
                              HarmonyItem, Scale, TimeSignature)
from beethoven.sequencer.objects import (HarmonyItemSelector,
                                        InvalidHarmonyChordItems)

a_major = Scale.parse("A_major")
d_minor = Scale.parse("D_minor")
g_mixolydian = Scale.parse("G_mixolydian")

chord_item_11 = ChordItem(root=Degree("II"), name="", duration_item=Duration())
chord_item_12 = ChordItem(root=Degree("V"), name="", duration_item=Duration())
chord_item_13 = ChordItem(root=Degree("I"), name="", duration_item=Duration())
chord_item_21 = ChordItem(root=Degree("II"), name="", duration_item=Duration())
chord_item_22 = ChordItem(root=Degree("V"), name="", duration_item=Duration())
chord_item_23 = ChordItem(root=Degree("I"), name="", duration_item=Duration())
chord_item_24 = ChordItem(root=Degree("IV"), name="", duration_item=Duration())
chord_item_31 = ChordItem(root=Degree("VI"), name="", duration_item=Duration())
chord_item_32 = ChordItem(root=Degree("III"), name="", duration_item=Duration())

@fixture
def harmony_item_1():
    return HarmonyItem(
        scale=a_major,
        chord_items=[chord_item_11, chord_item_12, chord_item_13],
        bpm=Bpm(120),
        time_signature=TimeSignature(4, 4)
    )

@fixture
def harmony_item_2():
    return HarmonyItem(
        scale=d_minor,
        chord_items=[chord_item_21, chord_item_22, chord_item_23],
        bpm=Bpm(90),
        time_signature=TimeSignature(6, 4)
    )

@fixture
def harmony_item_3():
    return HarmonyItem(
        scale=g_mixolydian,
        chord_items=[chord_item_31],
        bpm=Bpm(75),
        time_signature=TimeSignature(3, 2)
    )

@fixture
def harmony_selector(harmony_item_1, harmony_item_2):
    return HarmonyItemSelector([harmony_item_1, harmony_item_2])


def test_harmony_item_selector(harmony_selector, harmony_item_1, harmony_item_2):
    origin_items = (harmony_item_1, chord_item_11)

    assert harmony_selector.current_items == origin_items

    assert harmony_selector.get_next_items()[0] == (harmony_item_1, chord_item_12)
    assert harmony_selector.get_next_items()[1] == (0, 1)

    assert harmony_selector.get_previous_items()[0] == (harmony_item_2, chord_item_23)
    assert harmony_selector.get_previous_items()[1] == (1, 2)

    for _, expected in zip(range(6), [(0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (0, 0)]):
        harmony_selector.next()

        assert harmony_selector.current_indexes == expected

    for _, expected in zip(range(6), [(1, 2), (1, 1), (1, 0), (0, 2), (0, 1), (0, 0)]):
        harmony_selector.previous()
        
        assert harmony_selector.current_indexes == expected

    assert harmony_selector.current_items == origin_items


def test_harmony_item_selector_with_chords_looping(harmony_selector, harmony_item_1, harmony_item_2):
    origin_items = (harmony_item_1, chord_item_11)

    harmony_selector.set_chord_looping(True)

    assert harmony_selector.current_items == origin_items

    assert harmony_selector.get_next_items()[0] == (harmony_item_1, chord_item_12)
    assert harmony_selector.get_next_items()[1] == (0, 1)

    harmony_selector.next()

    assert harmony_selector.get_next_items()[0] == (harmony_item_1, chord_item_13)
    assert harmony_selector.get_next_items()[1] == (0, 2)

    harmony_selector.next()

    assert harmony_selector.get_next_items()[0] == (harmony_item_1, chord_item_11)
    assert harmony_selector.get_next_items()[1] == (0, 0)

    harmony_selector.next()

    assert harmony_selector.current_items == origin_items

    assert harmony_selector.get_previous_items()[0] == (harmony_item_1, chord_item_13)
    assert harmony_selector.get_previous_items()[1] == (0, 2)

    harmony_selector.previous()

    harmony_selector.set_chord_looping(False)

    assert harmony_selector.get_next_items()[0] == (harmony_item_2, chord_item_21)
    assert harmony_selector.get_next_items()[1] == (1, 0)


def test_harmony_item_selector_set_reset_functions(harmony_selector, harmony_item_1, harmony_item_2):
    harmony_selector.set(harmony_item_1, chord_item_11)

    assert harmony_selector.current_indexes == (0, 0)

    harmony_selector.set(harmony_item_1, chord_item_13)

    assert harmony_selector.current_indexes == (0, 2)

    harmony_selector.set(harmony_item_2, chord_item_21)

    assert harmony_selector.current_indexes == (1, 0)

    with raises(InvalidHarmonyChordItems):
        harmony_selector.set(harmony_item_1, chord_item_21)

    harmony_selector.reset()

    assert harmony_selector.current_indexes == (0, 0)

def test_harmony_item_selector_insert_functions(harmony_selector, harmony_item_1, harmony_item_2, harmony_item_3):
    harmony_selector = HarmonyItemSelector([harmony_item_1, harmony_item_2])

    harmony_selector.set(harmony_item_2, harmony_item_2.chord_items[-1])
    harmony_selector.insert(chord_item_24)

    assert harmony_item_2.chord_items == [chord_item_21, chord_item_22, chord_item_23, chord_item_24]
    assert len(harmony_selector.harmony_items) == 2

    harmony_selector.insert(harmony_item_3)

    assert harmony_selector.harmony_items == [harmony_item_1, harmony_item_2, harmony_item_3]

    harmony_selector.set(harmony_item_3, harmony_item_3.chord_items[-1])

    assert len(harmony_item_3.chord_items) == 1

    harmony_selector.insert(chord_item_32)

    assert harmony_item_3.chord_items == [chord_item_31, chord_item_32]


def test_harmony_item_selector_delete_functions(harmony_selector, harmony_item_1, harmony_item_2):
    harmony_selector.set(harmony_item_2, harmony_item_2.chord_items[-1])
    harmony_selector.delete(ChordItem)

    assert harmony_item_2.chord_items == [chord_item_21, chord_item_22]

    harmony_selector.set(harmony_item_2, harmony_item_2.chord_items[0])
    harmony_selector.delete(ChordItem)

    assert harmony_item_2.chord_items == [chord_item_22]

    harmony_selector.delete(HarmonyItem)

    assert harmony_selector.harmony_items == [harmony_item_1]

    harmony_selector.set(harmony_item_1, harmony_item_1.chord_items[-1])

    harmony_selector.delete(ChordItem)
    harmony_selector.delete(ChordItem)

    assert len(harmony_item_1.chord_items) == 1

    harmony_selector.delete(ChordItem)

    assert len(harmony_item_1.chord_items) == 1

    harmony_selector.delete(HarmonyItem)

    assert harmony_selector.harmony_items == [harmony_item_1]
