from pytest import mark, raises

from beethoven.sequencer.chord import Chord
from beethoven.sequencer.note import Note


@mark.parametrize("root_note,chord_name,result_notes", [
    ("A3", "maj",      "A3,C#4,E4"),
    ("B4", "min",      "B4,D5,F#5"),
    ("D5", "maj7",     "D5,F#5,A5,C#6"),
    ("F6", "min maj7", "F6,Ab6,C7,E7")
])
def test_chord_instanciation(root_note, chord_name, result_notes):
    chord = Chord(root_note, chord_name)

    assert chord.notes == Note.to_list(result_notes)


def test_chord_instanciation_without_attrubutes():
    with raises(ValueError, match="Chord name and root note must be set"):
        Chord()


@mark.parametrize("root_note,chord_name,base_note,expected_str", [
    ("A4", "maj",      "G3",  "A4maj/G3"),
    ("B4", "min",      "A3",  "B4min/A3"),
    ("D3", "maj7",     "B2",  "D3maj7/B2"),
    ("F3", "min maj7", "C#3", "F3min maj7/C#3")
])
def test_chord_instanciation_with_base_note(root_note, chord_name, base_note, expected_str):
    chord = Chord(root_note, chord_name, base_note=base_note)

    assert chord.base_note == Note(base_note)
    assert repr(chord) == f"<Chord {expected_str}>"


def test_chord_instanciation_with_inversion():
    normal = Chord("A4", "power", inversion=0)
    inverted = Chord("A4", "power", inversion=1)

    assert normal.notes == Note.to_list("A4,E5")
    assert inverted.notes == Note.to_list("E5,A5")


@mark.parametrize("inversion", [-1, 2])
def test_chord_instanciation_with_inversion_out_of_range(inversion):
    with raises(ValueError, match="Chord inversion out of range"):
        Chord("A4", "power", inversion=inversion)


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

    chord = FakeChord("A4", "test")
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
    root_note = "A4"

    notation1 = Chord(root_note, short)
    notation2 = Chord(root_note, extended)
    notation3 = Chord(root_note, symbol)

    assert notation1 == notation2
    assert notation2 == notation3

    assert str(notation1) == str(notation2)


@mark.parametrize("chord_name", ["foo", "bar"])
def test_chord_with_wrong_chord_name(chord_name):
    with raises(ValueError, match="Chord name does not exists"):
        Chord("A4", chord_name)


@mark.parametrize("chord_name", ["A3maj7", "Bb2min7", "C#3sus4", "E47"])
def test_chord_get_from_fullname_classmethod(chord_name):
    Chord.get_from_fullname(chord_name)


@mark.parametrize("chord_name", ["Hmaj7", "chord_name", "Atest_chord7"])
def test_chord_get_from_fullname_classmethod_no_match(chord_name):
    assert Chord.get_from_fullname(chord_name) is None
