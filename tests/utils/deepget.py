from pytest import mark

from beethoven.utils.deepget import deepget

TEST_DATA = {
    "mapping": {
        "sub_mapping": {"sub_key": "value1"},
        "array": ["item0", "item1", "item2"],
        "key": "value2",
        "bool": False,
    },
    "array": [1, 2, 3, 4],
    "bool": True,
}


@mark.parametrize(
    "path,result",
    [
        ("mapping.sub_mapping.sub_key", "value1"),
        ("mapping.array.1", "item1"),
        ("mapping.key", "value2"),
        ("mapping.bool", False),
        ("array", [1, 2, 3, 4]),
        ("bool", True),
        ("non_existing_key", None),
        (["mapping", "sub_mapping", "sub_key"], "value1"),
    ],
)
def test_deepget(path, result):
    assert deepget(TEST_DATA, path) == result
