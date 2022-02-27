from pytest import raises

from beethoven.models import Chord, Note


def test_chord_model():
    assert Chord(root=Note(name="C"), name="maj7")


def test_chord_model_raise_invalid_name():
    with raises(ValueError, match="Invalid name: fake"):
        Chord(root=Note(name="C"), name="fake")
