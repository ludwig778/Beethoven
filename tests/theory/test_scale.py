from pytest import mark, raises

from beethoven.theory.chord import Chord
from beethoven.theory.note import Note
from beethoven.theory.scale import Scale


@mark.parametrize("root_note,scale_name,result_notes", [
    ("A", "major",       "A,B,C#,D,E,F#,G#"),
    ("B", "minor",       "B,C#,D,E,F#,G,A"),
    ("D", "phrygian #6", "D,Eb,F,G,A,B,C"),
    ("F", "whole tone",  "F,G,A,B,Db,Eb")
])
def test_scale(root_note, scale_name, result_notes):
    scale = Scale(root_note, scale_name)

    assert scale.notes == Note.to_list(result_notes)


def test_scale_instanciation_without_attributes():
    with raises(ValueError, match="Scale name and tonic note must be set"):
        Scale()


@mark.parametrize("scale_name", ["foo", "bar"])
def test_scale_with_wrong_scale_name(scale_name):
    with raises(ValueError, match="Scale name does not exists"):
        Scale("A", scale_name)


@mark.parametrize("start_degree_name,chord_basic,chord_seventh", [
    (1, Chord("B",  "min"), Chord("B",  "min7")),
    (2, Chord("C#", "min"), Chord("C#", "min7")),
    (3, Chord("D",  "maj"), Chord("D",  "maj7")),
    (4, Chord("E",  "maj"), Chord("E",  "7")),
    (6, Chord("G#", "dim"), Chord("G#", "min7b5")),
])
def test_scale_get_chord(start_degree_name, chord_basic, chord_seventh):
    scale = Scale("A", "major")

    assert scale.get_chord(start_degree_name, "1,3,5") == chord_basic
    assert scale.get_chord(start_degree_name, "1,3,5,7") == chord_seventh


@mark.parametrize("start_degree_name,alteration,chord_basic,chord_seventh", [
    (1, 0,  Chord("B",   "min"), Chord("B",   "min7")),
    (1, 1,  Chord("B#",  "min"), Chord("B#",  "min7")),
    (1, 2,  Chord("B##", "min"), Chord("B##", "min7")),
    (1, -2, Chord("Bbb", "min"), Chord("Bbb", "min7")),
])
def test_scale_get_chord_with_alteration(start_degree_name, alteration, chord_basic, chord_seventh):
    scale = Scale("A", "major")

    assert scale.get_chord(start_degree_name, "1,3,5", alteration=alteration) == chord_basic
    assert scale.get_chord(start_degree_name, "1,3,5,7", alteration=alteration) == chord_seventh


@mark.parametrize("name,alt_name", [
    ('ionian', 'major'),
    ('aeolian', 'minor'),
    ('melodic minor', 'ascending melodic minor'),
])
def test_scale_notation_on_initialization(name, alt_name):
    root_note = "A"

    notation1 = Scale(root_note, name)
    notation2 = Scale(root_note, alt_name)

    assert notation1 == notation2
    assert repr(notation1) == repr(notation2)


def test_scale_instanciation_through_to_dict():
    scale = Scale("A", "major")

    assert scale == Scale(**scale.to_dict())


@mark.parametrize("base_scale,mode_switch,target_scale", [
    (Scale("A", "major"),                 2, Scale("A", "phrygian")),
    (Scale("A", "major"),                 4, Scale("A", "mixolydian")),
    (Scale("A", "major"),                 6, Scale("A", "locrian")),
    (Scale("A", "melodic minor"),         3, Scale("A", "lydian dominant")),
    (Scale("A", "harmonic minor"),        6, Scale("A", "altered diminished")),
    (Scale("A", "double harmonic minor"), 1, Scale("A", "lydian #2 #6")),
])
def test_scale_switch_mode(base_scale, mode_switch, target_scale):
    assert base_scale.switch_mode(mode_switch) == target_scale


def test_scale_raise_on_switch_mode():
    with raises(ValueError, match="Scale doesnt have modes"):
        Scale("A", "pentatonic").switch_mode(2)
