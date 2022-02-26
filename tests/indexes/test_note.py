def test_note_index_get_names(indexes):
    assert indexes.notes.get_names("C") == ["C", "Do"]


def test_note_index_get_index(indexes):
    assert indexes.notes.get_index("C") == 0
    assert indexes.notes.get_index("B") == 6


def test_note_index_get_semitones(indexes):
    assert indexes.notes.get_semitones("C") == 0
    assert indexes.notes.get_semitones("B") == 11


def test_note_index_get_name_from_index(indexes):
    assert indexes.notes.get_name_from_index(0) == "C"
    assert indexes.notes.get_name_from_index(6) == "B"
