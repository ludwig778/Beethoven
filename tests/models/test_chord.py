from pytest import mark

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
