def test_scale_index_get_names(indexes):
    assert indexes.scales.get_names("pentatonic") == ["pentatonic minor", "pentatonic"]


def test_scale_index_get_intervals(indexes):
    assert indexes.scales.get_intervals("pentatonic") == "1,3m,4,5,7m"
    assert indexes.scales.get_intervals("lydian") == "1,2,3,4a,5,6,7"
