from pytest import mark, raises

from beethoven.exceptions import InversionOutOfRange, ScaleIsNotDiatonic
from beethoven.mappings import chord_mapping
from beethoven.objects import Chord, Interval, Note, Scale


@mark.parametrize(
    "string,intervals,notes",
    [
        ("A_maj", "1,3,5", "A,C#,E"),
        ("B_min", "1,3m,5", "B,D,F#"),
        ("C_maj7", "1,3,5,7", "C,E,G,B"),
        ("D_7", "1,3,5,7m", "D,F#,A,C"),
        ("E5_add5", "1,5", "E5,B5"),
        ("F4_dim7", "1,3m,5d,7d", "F4,Ab4,Cb5,Ebb5"),
        ("G_min_6", "1,3m,5,6", "G,Bb,D,E"),
    ],
)
def test_simple_chord_parsing(string, intervals, notes):
    chord = Chord.parse(string)

    assert chord.notes == Note.parse_list(notes)
    assert chord.intervals == Interval.parse_list(intervals)


@mark.parametrize(
    "string",
    [
        "A_major_triad_(b5)",
        "A_major_7_(#5)",
        "A_-",
        "A_+",
        "A_°",
        "A_Δ",
        "A_ø",
        "A_7",
    ],
)
def test_chord_parsing_with_symbols(string):
    assert Chord.parse(string)


@mark.parametrize(
    "string,notes",
    [
        ("A4:i=0", "A4,C#5,E5"),
        ("A4:i=1", "C#5,E5,A5"),
        ("A4:i=2", "E5,A5,C#6"),
    ],
)
def test_chord_parsing_with_inversion(string, notes):
    chord = Chord.parse(string)

    assert chord.notes == Note.parse_list(notes)


def test_chord_parsing_with_out_of_range_inversion():
    with raises(InversionOutOfRange):
        Chord.parse("A4:i=3")


@mark.parametrize(
    "string,extensions,notes",
    [
        ("A:e=9", "9", "A,C#,E,B"),
        ("A:e=11,13m", "11,13m", "A,C#,E,D,F"),
        ("A4:e=9", "9", "A4,C#5,E5,B5"),
        ("A4:e=11,13m", "11,13m", "A4,C#5,E5,D6,F6"),
    ],
)
def test_chord_parsing_with_extensions(string, extensions, notes):
    chord = Chord.parse(string)

    assert chord.notes == Note.parse_list(notes)
    assert chord.extensions == Interval.parse_list(extensions)


@mark.parametrize(
    "string,notes",
    [
        ("A:b=D", "D,A,C#,E"),
        ("A4:b=D", "D4,A4,C#5,E5"),
        ("A4:b=D2", "D2,A4,C#5,E5"),
        ("A4:b=B", "B3,A4,C#5,E5"),
        ("A4:b=B5", "B3,A4,C#5,E5"),
    ],
)
def test_chord_parsing_with_base_note(string, notes):
    chord = Chord.parse(string)

    assert chord.notes == Note.parse_list(notes)


@mark.parametrize(
    "string,intervals,extensions,notes",
    [
        ("A:i=0:b=G:e=6", "1,3,5", "6", "G,A,C#,E,F#"),
        ("A4:i=0:b=G:e=6", "1,3,5", "6", "G4,A4,C#5,E5,F#5"),
        ("A4:i=1:b=G:e=6", "1,3,5", "6", "G4,C#5,E5,A5,F#5"),
        ("C4_maj7:b=A2:e=9", "1,3,5,7", "9", "A2,C4,E4,G4,B4,D5"),
        ("C4_maj7:i=3:b=A2:e=9", "1,3,5,7", "9", "A2,B4,C5,E5,G5,D5"),
        ("C4_maj7:i=3:b=A:e=9,11,13", "1,3,5,7", "9,11,13", "A4,B4,C5,E5,G5,D5,F5,A5"),
    ],
)
def test_full_chord_parsing(string, intervals, extensions, notes):
    chord = Chord.parse(string)

    assert chord.notes == Note.parse_list(notes)
    assert chord.intervals == Interval.parse_list(intervals)
    assert chord.extensions == Interval.parse_list(extensions)


@mark.parametrize(
    "intervals,chord_name",
    [
        ("1,3,5,7", "maj7"),
    ],
)
def test_get_from_intervals(intervals, chord_name):
    assert chord_mapping.get_name_from_intervals(intervals) == chord_name


@mark.parametrize(
    "scale,chords",
    [
        ("C_ionian", "C_maj7,D_min7,E_min7,F_maj7,G_7,A_min7,B_min7"),
        ("C_lydian", "C_maj7,D_7,E_min7,F#_min7,G_maj7,A_min7,B_min7"),
        ("G2_ionian", "G2_maj7,A2_min7,B2_min7,C3_maj7,D3_7,E3_min7,F#3_min7"),
    ],
)
def test_get_chords_from_scale(scale, chords):
    scale = Scale.parse(scale)

    assert Chord.serialize_list(scale.get_chords()) == chords


@mark.parametrize(
    "scale,chords",
    [
        ("C_ionian", "C_maj,D_min,E_min,F_maj,G_maj,A_min,B_min"),
        ("C_lydian", "C_maj,D_maj,E_min,F#_min,G_maj,A_min,B_min"),
        ("G2_ionian", "G2_maj,A2_min,B2_min,C3_maj,D3_maj,E3_min,F#3_min"),
    ],
)
def test_get_chords_from_scale_with_triad_degrees(scale, chords):
    scale = Scale.parse(scale)

    assert Chord.serialize_list(scale.get_chords([1, 3, 5])) == chords


@mark.parametrize(
    "scale,chord,notes",
    [
        ("C", "I", "C,E,G,B"),
        ("C", "V", "G,B,D,F"),
        ("E4_lydian", "I", "E4,G#4,B4,D#5"),
        ("G2_minor", "II", "A2,C3,E3,G3"),
    ],
)
def test_chord_parsing_with_degrees(scale, chord, notes):
    scale = Scale.parse(scale)
    chord = Chord.parse(chord, scale=scale)

    assert chord.notes == Note.parse_list(notes)


@mark.parametrize(
    "scale,chord,notes",
    [
        ("C", "V:s=II", "A,C#,E,G"),
        ("C", "V:s=III", "B,D#,F#,A"),
        ("C", "V:s=IV", "C,E,G,Bb"),
        ("C4", "V:s=V", "D5,F#5,A5,C6"),
        ("C4", "V:s=VI", "E5,G#5,B5,D6"),
    ],
)
def test_chord_parsing_with_base_degrees(scale, chord, notes):
    scale = Scale.parse(scale)
    chord = Chord.parse(chord, scale=scale)

    assert chord.notes == Note.parse_list(notes)


def test_chord_parsing_with_not_diatonic_scale():
    scale = Scale.parse("A_pentatonic")

    with raises(ScaleIsNotDiatonic, match="Scale A_pentatonic is not diatonic"):
        Chord.parse("V", scale=scale)
