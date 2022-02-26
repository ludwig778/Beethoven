from pytest import mark

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
