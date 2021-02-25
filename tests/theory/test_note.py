from pytest import mark, raises

from beethoven.theory.interval import Interval
from beethoven.theory.note import Note, NoteNameContainer


@mark.parametrize("anglosaxon,solfege", [("A", "La"), ("C#", "Do#"), ("Eb", "Mib"), ("G", "Sol")])
def test_note_check_display_note_name_change(anglosaxon, solfege):
    note = Note(anglosaxon)

    assert str(note) == f"<Note {anglosaxon}>"
    NoteNameContainer.set(1)

    assert str(note) == f"<Note {solfege}>"
    NoteNameContainer.set(0)


def test_note_instanciation_without_attributes():
    with raises(ValueError, match="Note name must be set"):
        Note()


def test_note_with_empty_note_name():
    with raises(ValueError, match="Note name does not exists"):
        Note("")


@mark.parametrize("note_name", ["foo", "bar", "baz"])
def test_note_with_wrong_note_name(note_name):
    with raises(ValueError, match="Note name does not exists"):
        Note(note_name)


@mark.parametrize("anglosaxon,solfege", [("A", "La"), ("G", "Sol")])
def test_note_is_the_same_between_notation_systems(anglosaxon, solfege):
    note_a, note_s = Note(anglosaxon), Note(solfege)

    assert note_a == note_s
    assert note_a is not None


@mark.parametrize("anglosaxon,solfege", [("Ab", "Lab"), ("Gb", "Solb")])
def test_note_is_the_same_between_notation_systems_with_flats(anglosaxon, solfege):
    note_a, note_s = Note(anglosaxon), Note(solfege)

    assert note_a == note_s
    assert note_a is not None


@mark.parametrize("anglosaxon,solfege", [("A#", "La#"), ("G#", "Sol#")])
def test_note_is_the_same_between_notation_systems_with_sharps(anglosaxon, solfege):
    note_a, note_s = Note(anglosaxon), Note(solfege)

    assert note_a == note_s
    assert note_a is not None


@mark.parametrize("note_name", ["Ab#", "C##bb", "G#b"])
def test_note_with_sharps_and_flats_raise_exception(note_name):
    with raises(ValueError, match="Note name shouldn't contain sharps AND flats"):
        Note(note_name)


@mark.parametrize("note_name,interval_name,result_note_name", [
    ("A", "3m", "C"),
    ("A", "3", "C#"),
    ("A", "4dd", "Dbb"),
])
def test_note_add_interval_method(note_name, interval_name, result_note_name):
    assert Note(note_name) + Interval(interval_name) == Note(result_note_name)


@mark.parametrize("note_name,interval_name,result_note_name", [
    ("C", "3m", "A"),
    ("C#", "3", "A"),
    ("Dbb", "4dd", "A"),
])
def test_note_substract_interval_method(note_name, interval_name, result_note_name):
    assert Note(note_name) - Interval(interval_name) == Note(result_note_name)


def test_note_add_interval_with_non_interval_instance():
    assert Note("A").add_interval("3") == Note("C#")
    assert Note("G").add_interval("5", reverse=True) == Note("C")


def test_note_add_interval_with_non_interval_string():
    with raises(ValueError, match="Interval name does not exists"):
        Note("A").add_interval("test")


def test_note_comparison():
    assert Note("A") == Note("A")

    assert Note("A") < Note("B")

    assert Note("B") > Note("C")


def test_note_add_interval_alteration_normalization():
    assert Note("A") + Interval("1aaaaaaaaaaa") == Note("Ab")
    assert Note("A") + Interval("1ddddddddddd") == Note("A#")


def test_note_instanciation_through_to_dict():
    note = Note("A")

    assert note == Note(**note.to_dict())
