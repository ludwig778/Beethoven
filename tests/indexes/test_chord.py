from beethoven.indexes import chord_index


def test_chord_index_is_valid():
    assert chord_index.is_valid("power")

    assert not chord_index.is_valid("fake")


def test_chord_index_get_names():
    assert chord_index.get_names("power") == ["power", "power_chord", "add5"]


def test_chord_index_get_intervals():
    assert chord_index.get_intervals("power") == "1,5"
    assert chord_index.get_intervals("maj7") == "1,3,5,7"


def test_chord_index_get_name_from_intervals():
    assert chord_index.get_name_from_intervals("1,3,5,7") == "maj7"
