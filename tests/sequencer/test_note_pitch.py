from pytest import mark

from beethoven.sequencer.note import Note, NoteNameContainer


@mark.parametrize("note_name", ["A#4", "C5", "Dbb6", "F##3", "G5"])
def test_note_instanciation(note_name):
    assert Note(note_name)


@mark.parametrize("anglosaxon,solfege", [("A4", "La4"), ("C#6", "Do#6"), ("Eb5", "Mib5"), ("G7", "Sol7")])
def test_note_check_display_note_name_change(anglosaxon, solfege):
    note = Note(anglosaxon)

    assert str(note) == f"<Note {anglosaxon}>"
    NoteNameContainer.set(1)

    assert str(note) == f"<Note {solfege}>"
    NoteNameContainer.set(0)


"""
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
    assert Note(note_name).add_interval(interval_name) == Note(result_note_name)
"""
