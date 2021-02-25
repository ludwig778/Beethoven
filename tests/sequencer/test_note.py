from pytest import mark, raises

from beethoven.sequencer.interval import Interval
from beethoven.sequencer.note import Note, NoteNameContainer
from beethoven.theory.note import Note as BaseNote


@mark.parametrize("anglosaxon,solfege", [("A2", "La2"), ("C#3", "Do#3"), ("Eb3", "Mib3"), ("G4", "Sol4")])
def test_note_check_display_note_name_change(anglosaxon, solfege):
    note = Note(anglosaxon)

    assert str(note) == f"<Note {anglosaxon}>"
    NoteNameContainer.set(1)

    assert str(note) == f"<Note {solfege}>"
    NoteNameContainer.set(0)


def test_note_with_empty_note_name():
    with raises(ValueError, match="Note could not be parsed"):
        Note("")


def test_note_instanciation_without_attributes():
    with raises(ValueError, match="Note name must be set"):
        Note()


@mark.parametrize("note_name", ["foo", "bar", "baz"])
def test_note_with_wrong_note_name(note_name):
    with raises(ValueError, match="Note could not be parsed"):
        Note(note_name)


@mark.parametrize("anglosaxon,solfege", [("A4", "La4"), ("G4", "Sol4")])
def test_note_is_the_same_between_notation_systems(anglosaxon, solfege):
    note_a, note_s = Note(anglosaxon), Note(solfege)

    assert note_a == note_s
    assert note_a is not None


@mark.parametrize("anglosaxon,solfege", [("Ab3", "Lab3"), ("Gb3", "Solb3")])
def test_note_is_the_same_between_notation_systems_with_flats(anglosaxon, solfege):
    note_a, note_s = Note(anglosaxon), Note(solfege)

    assert note_a == note_s
    assert note_a is not None


@mark.parametrize("anglosaxon,solfege", [("A#2", "La#2"), ("G#2", "Sol#2")])
def test_note_is_the_same_between_notation_systems_with_sharps(anglosaxon, solfege):
    note_a, note_s = Note(anglosaxon), Note(solfege)

    assert note_a == note_s
    assert note_a is not None


@mark.parametrize("note_name", ["Ab#2", "C##bb3", "G#b4"])
def test_note_with_sharps_and_flats_raise_exception(note_name):
    with raises(ValueError, match="Note name shouldn't contain sharps AND flats"):
        Note(note_name)


@mark.parametrize("note_name,interval_name,result_note_name", [
    ("A3", "3m",  "C4"),
    ("A3", "3",   "C#4"),
    ("A3", "4dd", "Dbb4"),
])
def test_note_add_interval_method(note_name, interval_name, result_note_name):
    assert Note(note_name) + Interval(interval_name) == Note(result_note_name)


@mark.parametrize("note_name,interval_name,result_note_name", [
    ("C4",   "3m",  "A3"),
    ("C#4",  "3",   "A3"),
    ("Dbb4", "4dd", "A3"),
])
def test_note_substract_interval_method(note_name, interval_name, result_note_name):
    assert Note(note_name) - Interval(interval_name) == Note(result_note_name)


def test_note_add_interval_with_non_interval_instance():
    assert Note("A3").add_interval("3") == Note("C#4")
    assert Note("G3").add_interval("5", reverse=True) == Note("C3")


def test_note_add_interval_with_non_interval_string():
    with raises(ValueError, match="Interval name does not exists"):
        Note("A4").add_interval("test")


def test_note_comparison():
    assert Note("A4") == Note("A4")

    assert Note("A2") < Note("B2")

    assert Note("B3") > Note("C2")


def test_note_add_interval_alteration_normalization():
    assert Note("A4") + Interval("1aaaaaaaaaaa") == Note("Ab4")
    assert Note("A4") + Interval("1ddddddddddd") == Note("A#4")


def test_note_casting_to_theory_self():
    return BaseNote("B") == Note("B4").get_theory_self()
