from pytest import mark, raises

from beethoven.theory.interval import Interval, IntervalNameContainer


@mark.parametrize("interval_name", ["2m", "9a", "7d", "4a", "13M", "6m", "5dd"])
def test_interval_check_display(interval_name):
    assert str(Interval(interval_name)) == f"<Interval {interval_name.replace('M', '')}>"


@mark.parametrize("interval_name,interval_display", [
    ("2m", "minor second"),
    ("3", "major third"),
    ("5a", "augmented fifth"),
    ("6a", "augmented sixth"),
    ("7d", "diminished seventh"),
    ("4d", "diminished fourth"),
    ("4", "perfect fourth"),
    ("8", "octave")
])
def test_interval_check_fullname_display(interval_name, interval_display):
    IntervalNameContainer.set(1)
    assert str(Interval(interval_name)) == f"<Interval {interval_display}>"
    IntervalNameContainer.set(0)


def test_note_instanciation_without_attributes():
    with raises(ValueError, match="Interval name must be set"):
        Interval()


@mark.parametrize("interval_name", ["4M", "5M"])
def test_interval_with_major_alteration_on_perfect_interval(interval_name):
    with raises(ValueError, match="Major alteration on perfect interval is not possible"):
        Interval(interval_name)


@mark.parametrize("interval_name", ["4m", "5m"])
def test_interval_with_minor_alteration_on_perfect_interval(interval_name):
    with raises(ValueError, match="Minor alteration on perfect interval is not possible"):
        Interval(interval_name)


@mark.parametrize("interval_name", ["3", "6"])
def test_interval_with_implicit_major(interval_name):
    assert Interval(interval_name) == Interval(interval_name + "M")


@mark.parametrize("interval_name", ["foo", "bar", "15"])
def test_interval_with_wrong_interval_name(interval_name):
    with raises(ValueError, match="Interval name does not exists"):
        Interval(interval_name)


@mark.parametrize("interval_name", ["3ad", "7mM"])
def test_interval_impossible_interval_alterations(interval_name):
    msg = "Interval alteration should be of a single type M, m, a or d"
    with raises(ValueError, match=msg):
        Interval(interval_name)


@mark.parametrize("interval_name", ["3ad", "7mM"])
def test_interval_with_multiple_alterations(interval_name):
    msg = "Interval alteration should be of a single type M, m, a or d"
    with raises(ValueError, match=msg):
        Interval(interval_name)


@mark.parametrize("interval_name", ["25", "unissson"])
def test_interval_initialization_with_a_non_existing_interval_name(interval_name):
    with raises(ValueError, match="Interval name does not exists"):
        Interval(interval_name)


@mark.parametrize("interval_name,error_msg", [
    ("1M", "Major alteration on unisson interval is not possible"),
    ("1m", "Minor alteration on unisson interval is not possible"),
    ("8M", "Major alteration on octave interval is not possible"),
    ("8m", "Minor alteration on octave interval is not possible"),
])
def test_interval_initialization_with_a_major_and_minor_perfect_intervals(interval_name, error_msg):
    with raises(ValueError, match=error_msg):
        Interval(interval_name)


def test_interval_is_hashable():
    {
        Interval("1"): "unisson",
        Interval("8"): "octave",
    }


def test_interval_comparison():
    assert Interval("1") <= Interval("1")

    assert Interval("1") < Interval("3")


def test_interval_instanciation_through_to_dict():
    interval = Interval("5")

    assert interval == Interval(**interval.to_dict())
