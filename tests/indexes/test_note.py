from beethoven.indexes import note_index


def test_note_index_get_names():
    assert note_index.get_names("C") == ["C", "Do"]


def test_note_index_get_index():
    assert note_index.get_index("C") == 0
    assert note_index.get_index("B") == 6


def test_note_index_get_semitones():
    assert note_index.get_semitones("C") == 0
    assert note_index.get_semitones("B") == 11


def test_note_index_get_name_from_index():
    assert note_index.get_name_from_index(0) == "C"
    assert note_index.get_name_from_index(6) == "B"
