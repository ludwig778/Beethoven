from pytest import raises

from beethoven.models import Note, Scale


def test_scale_model():
    assert Scale(tonic=Note(name="C"), name="major")


def test_scale_model_raise_invalid_name():
    with raises(ValueError, match="Invalid name: fake"):
        Scale(tonic=Note(name="C"), name="fake")
