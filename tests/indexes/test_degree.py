from beethoven.indexes import degree_index


def test_degree_index_is_valid():
    assert degree_index.is_valid("i")

    assert not degree_index.is_valid("viii")


def test_degree_index_get_name():
    assert degree_index.get_name(0) == "i"
    assert degree_index.get_name(6) == "vii"


def test_degree_index_get_index():
    assert degree_index.get_index("I") == 0
    assert degree_index.get_index("IV") == 3
    assert degree_index.get_index("vii") == 6
