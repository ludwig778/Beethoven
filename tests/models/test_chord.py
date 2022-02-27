from pytest import mark, raises

from beethoven.models import Chord, Note


@mark.parametrize(
    "root,name",
    [
        [Note(name="C"), "maj7"],
        [Note(name="G"), "min7"],
    ],
)
def test_chord_model(root, name):
    assert Chord(root=root, name=name)


def test_chord_model_raise_invalid_name():
    with raises(ValueError, match="Invalid name: fake"):
        Chord(root=Note(name="C"), name="fake")
