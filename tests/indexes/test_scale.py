from beethoven.indexes import scale_index


def test_scale_index_is_valid():
    assert scale_index.is_valid("pentatonic")

    assert not scale_index.is_valid("test")


def test_scale_index_get_names():
    assert scale_index.get_names("pentatonic") == ["pentatonic minor", "pentatonic"]


def test_scale_index_get_intervals():
    assert scale_index.get_intervals("pentatonic") == "1,3m,4,5,7m"
    assert scale_index.get_intervals("lydian") == "1,2,3,4a,5,6,7"
