from pytest import mark

from beethoven import controllers
from beethoven.models import Interval


@mark.parametrize(
    "string,expected",
    [
        ["1", Interval(name="1")],
        ["3M", Interval(name="3")],
        ["4", Interval(name="4")],
        ["4a", Interval(name="4", alteration=1)],
        ["5d", Interval(name="5", alteration=-1)],
        ["6m", Interval(name="6", alteration=-1)],
        ["7d", Interval(name="7", alteration=-2)],
        ["8", Interval(name="8")],
        ["8a", Interval(name="8", alteration=1)],
        ["10M", Interval(name="10")],
        ["11", Interval(name="11")],
        ["11a", Interval(name="11", alteration=1)],
        ["12d", Interval(name="12", alteration=-1)],
        ["13m", Interval(name="13", alteration=-1)],
        ["14d", Interval(name="14", alteration=-2)],
        ["15", Interval(name="15")],
    ],
)
def test_interval_parser(string, expected):
    assert controllers.interval.parse(string) == expected


@mark.parametrize(
    "string,expected",
    [
        [
            "1,2,3,4,5,6,7",
            [
                Interval(name="1"),
                Interval(name="2"),
                Interval(name="3"),
                Interval(name="4"),
                Interval(name="5"),
                Interval(name="6"),
                Interval(name="7"),
            ],
        ],
        [
            "1,3m,4,5,7m",
            [
                Interval(name="1"),
                Interval(name="3", alteration=-1),
                Interval(name="4"),
                Interval(name="5"),
                Interval(name="7", alteration=-1),
            ],
        ],
        [
            "1,2,3,4a,5,6,7",
            [
                Interval(name="1"),
                Interval(name="2"),
                Interval(name="3"),
                Interval(name="4", alteration=1),
                Interval(name="5"),
                Interval(name="6"),
                Interval(name="7"),
            ],
        ],
    ],
)
def test_interval_list_parser(string, expected):
    assert controllers.interval.parse_list(string) == expected
