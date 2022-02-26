def test_interval_index_get_names(indexes):
    assert indexes.intervals.get_names("1") == ["1", "unisson"]


def test_interval_index_get_index(indexes):
    assert indexes.intervals.get_index("1") == 0
    assert indexes.intervals.get_index("7") == 6


def test_interval_index_get_semitones(indexes):
    assert indexes.intervals.get_semitones("1") == 0
    assert indexes.intervals.get_semitones("7") == 11


def test_interval_index_get_name_from_index(indexes):
    assert indexes.intervals.get_name_from_index(0) == "1"
    assert indexes.intervals.get_name_from_index(6) == "7"
