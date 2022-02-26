def test_chord_index_get_names(indexes):
    assert indexes.chords.get_names("power") == ["power", "power chord", "add5"]


def test_chord_index_get_intervals(indexes):
    assert indexes.chords.get_intervals("power") == "1,5"
    assert indexes.chords.get_intervals("maj7") == "1,3,5,7"


def test_chord_index_get_name_from_intervals(indexes):
    assert indexes.chords.get_name_from_intervals("1,3,5,7") == "maj7"
