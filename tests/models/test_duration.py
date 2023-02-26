from pytest import mark

from beethoven.models import Duration


@mark.parametrize(
    "string,expected_obj",
    [
        ["1", Duration.parse("1")],
        ["2", Duration.parse("2")],
        ["1/2", Duration.parse("1/2")],
        ["3/5", Duration.parse("3/5")],
        ["W", Duration.parse("4")],
        ["H", Duration.parse("2")],
        ["Q", Duration.parse("1")],
        ["E", Duration.parse("1/2")],
        ["S", Duration.parse("1/4")],
        ["1/4Q", Duration.parse("1/4")],
        ["1/5E", Duration.parse("1/10")],
        ["2/3S", Duration.parse("1/6")],
    ],
)
def test_duration_parsing(string, expected_obj):
    assert Duration.parse(string) == expected_obj
