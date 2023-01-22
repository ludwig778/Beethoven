from pytest import mark, raises

from beethoven.models import Bpm


@mark.parametrize(
    "string,expected_obj",
    [["20", Bpm(value=20)], ["60", Bpm(value=60)], ["120", Bpm(value=120)]],
)
def test_bpm_parsing(string, expected_obj):
    assert Bpm.parse(string) == expected_obj


@mark.parametrize("value", [60, 120])
def test_bpm_model(value):
    assert Bpm(value=value)


@mark.parametrize("value", [-1, 601])
def test_degree_model_raise_out_of_bound_value(value):
    with raises(ValueError, match=f"Invalid value: {value}, must be between 0 and 600"):
        Bpm(value=value)
