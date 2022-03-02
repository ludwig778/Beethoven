from pytest import raises

from beethoven.models import Note, Scale
from tests.fixtures.scales import a_minor, a_minor_pentatonic


def test_scale_model():
    assert Scale(tonic=Note(name="C"), name="major")


def test_scale_model_raise_invalid_name():
    with raises(ValueError, match="Invalid name: fake"):
        Scale(tonic=Note(name="C"), name="fake")


def test_scale_model_is_diatonic():
    assert a_minor.is_diatonic
    assert not a_minor_pentatonic.is_diatonic
