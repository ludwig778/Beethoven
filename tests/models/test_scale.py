from pytest import mark, raises

from beethoven.models import Note, Scale


@mark.parametrize(
    "tonic,name",
    [
        [Note(name="C"), "pentatonic"],
        [Note(name="G"), "major"],
    ],
)
def test_scale_model(tonic, name):
    assert Scale(tonic=tonic, name=name)


def test_scale_model_raise_invalid_name():
    with raises(ValueError, match="Invalid name: fake"):
        Scale(tonic=Note(name="C"), name="fake")
