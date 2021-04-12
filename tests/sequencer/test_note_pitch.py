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
