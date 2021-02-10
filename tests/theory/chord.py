from pytest import mark, raises

from beethoven.theory.chord import Chord
from beethoven.theory.note import Note


def to_list(notes):
    return [Note(n) for n in notes.split(",")]


@mark.parametrize("root_note,chord_name,result_notes", [
    ("A", "maj", "A,C#,E"),
    ("B", "min", "B,D,F#"),
    ("D", "maj7", "D,F#,A,C#"),
    ("F", "min maj7", "F,Ab,C,E")
])
def test_chord(root_note, chord_name, result_notes):
    chord = Chord(root_note, chord_name)

    assert chord.notes == to_list(result_notes)


def test_chord_name_container():
    class FakeChord(Chord):
        _DIRECTORY = {}

    short_notation = "test"
    extended_notation = "TESTING"
    symbol_notation = "t"
    mappings = [
        ('1', short_notation, extended_notation, symbol_notation)
    ]
    FakeChord.load(mappings)

    chord = FakeChord("A", "test")
    chord_name = chord.name

    assert chord_name.short == short_notation
    assert chord_name.extended == extended_notation
    assert chord_name.symbol == symbol_notation


@mark.parametrize("short,extended,symbol", [
    ('power', 'power chord', 'add5'),
    ('maj', 'major triad', ''),
    ('sus2', 'suspended 2', 'sus2'),
    ('min7', 'minor 7', '–7')
])
def test_chord_notation_on_initialization(short, extended, symbol):
    root_note = "A"

    notation1 = Chord(root_note, short)
    notation2 = Chord(root_note, extended)
    notation3 = Chord(root_note, symbol)

    assert notation1 == notation2
    assert notation2 == notation3

    assert str(notation1) == str(notation2)


@mark.parametrize("chord_name", ["foo", "bar"])
def test_chord_with_wrong_chord_name(chord_name):
    with raises(ValueError, match="Chord name does not exists"):
        Chord("A", chord_name)
