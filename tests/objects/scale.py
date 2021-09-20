from pytest import mark

from beethoven.objects import Interval, Note, Scale


@mark.parametrize(
    "scale_name,intervals,notes",
    [
        ("A_pentatonic", "1,3m,4,5,7m", "A,C,D,E,G"),
        ("B2_diminished", "1,3m,4a,6", "B2,D3,E#3,G#3"),
        ("C4_ionian", "1,2,3,4,5,6,7", "C4,D4,E4,F4,G4,A4,B4"),
        ("D3_dorian", "1,2,3m,4,5,6,7m", "D3,E3,F3,G3,A3,B3,C4"),
        ("E_lydian_#2_#6", "1,2a,3,4a,5,6a,7", "E,F##,G#,A#,B,C##,D#"),
        ("F_phrygian_bb7_b4", "1,2m,3m,4d,5,6m,7d", "F,Gb,Ab,Bbb,C,Db,Ebb"),
        (
            "G0_chromatic",
            "1,2m,2,3m,3,4,5d,5,6m,6,7m,7",
            "G0,Ab0,A0,Bb0,B0,C1,Db1,D1,Eb1,E1,F1,F#1",
        ),
    ],
)
def test_scale_parsing(scale_name, intervals, notes):
    scale = Scale.parse(scale_name)

    assert scale.notes == Note.parse_list(notes)
    assert scale.intervals == Interval.parse_list(intervals)


def test_scale_parsing_with_default_name():
    scale = Scale.parse("C")

    intervals = "1,2,3,4,5,6,7"
    notes = "C,D,E,F,G,A,B"

    assert scale.name == "ionian"

    assert scale.notes == Note.parse_list(notes)
    assert scale.intervals == Interval.parse_list(intervals)
