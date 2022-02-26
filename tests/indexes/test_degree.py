def test_degree_index_get_name(indexes):
    assert indexes.degrees.get_name(0) == "i"
    assert indexes.degrees.get_name(6) == "vii"


def test_degree_index_get_index(indexes):
    assert indexes.degrees.get_index("I") == 0
    assert indexes.degrees.get_index("IV") == 3
    assert indexes.degrees.get_index("vii") == 6
