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


def test_note_model_greater_equality_methods():
    assert Note(name="C") == Note(name="C")
    assert Note(name="C", alteration=1) == Note(name="C", alteration=1)
    assert Note(name="C", alteration=1, octave=4) == Note(
        name="C", alteration=1, octave=4
    )

    assert Note(name="C") != Note(name="C", alteration=1)

    # Check enharmonic notes
    assert Note(name="C") == Note(name="D", alteration=-2)


def test_note_model_greater_equality_methods_raise_octave_state_discrepancy():
    with raises(
        Exception, match="Octaves must be present or absent in order to compare Notes"
    ):
        Note(name="C") == Note(name="C", octave=1)


def test_note_model_greater_than_method():
    assert Note(name="C") < Note(name="B")
    assert Note(name="C", octave=1) > Note(name="B", octave=0)
    assert Note(name="C", octave=1) < Note(name="B", octave=1)

    assert Note(name="C") <= Note(name="D")
    assert Note(name="C") <= Note(name="B")
