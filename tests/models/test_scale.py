from pytest import mark

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
