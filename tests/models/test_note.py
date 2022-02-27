from pytest import mark, raises

from beethoven.models import Note


@mark.parametrize(
    "name,alteration,octave",
    [
        ["C", 0, None],
        ["G", 1, 4],
    ],
)
def test_note_model(name, alteration, octave):
    assert Note(name=name, alteration=alteration, octave=octave)


def test_note_model_raise_invalid_name():
    with raises(ValueError, match="Invalid name: H"):
        Note(name="H")


@mark.parametrize("alteration", [-4, 4])
def test_note_model_raise_invalid_alteration(alteration):
    with raises(
        ValueError, match=f"Invalid alteration: {alteration}, must be between -3 and 3"
    ):
        Note(name="C", alteration=alteration)


@mark.parametrize("octave", [-1, 11])
def test_note_model_raise_invalid_octave(octave):
    with raises(
        ValueError, match=f"Invalid octave: {octave}, must be between 0 and 10"
    ):
        Note(name="C", octave=octave)
