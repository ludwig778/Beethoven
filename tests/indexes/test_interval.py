from beethoven.indexes import interval_index


def test_interval_index_get_names():
    assert interval_index.get_names("1") == ["1", "unisson"]


def test_interval_index_get_index():
    assert interval_index.get_index("1") == 0
    assert interval_index.get_index("7") == 6


def test_interval_index_get_semitones():
    assert interval_index.get_semitones("1") == 0
    assert interval_index.get_semitones("7") == 11


def test_interval_index_get_name_from_index():
    assert interval_index.get_name_from_index(0) == "1"
    assert interval_index.get_name_from_index(6) == "7"
