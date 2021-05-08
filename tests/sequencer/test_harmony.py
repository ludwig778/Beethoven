from pytest import mark, raises

from beethoven.sequencer.chord import Chord
from beethoven.sequencer.harmony import Harmony
from beethoven.sequencer.scale import Scale


@mark.parametrize("scale_name", [
    ("ionian"),
    ("melodic minor"),
    ("harmonic minor"),
    ("double harmonic minor")
])
def test_harmony_instanciation_on_diatonic_scale(scale_name):
    Harmony(Scale("A4", scale_name))


@mark.parametrize("scale_name", [
    ("bebop"),
    ("chromatic"),
    ("pentatonic"),
    ("blues major"),
])
def test_harmony_instanciation_on_non_diatonic_scale(scale_name):
    with raises(ValueError, match="Scale given to harmony must be diatonic"):
        Harmony(Scale("A4", scale_name))


@mark.parametrize("degree_name,expected_chord", [
    ("i",       "A4min7"),
    ("I",       "A4maj7"),
    ("ii",      "B4min7"),
    ("II",      "B4min7"),
    ("bII",     "Bb4min7"),
    ("IV",      "D5maj7"),
    ("bIV",     "Db5maj7"),
    ("#V",      "E#57"),
    ("VI7",     "F#57"),
    ("VIIdim7", "G#5dim7"),
    ("vii",     "G#5min7b5"),
    ("viimin7", "G#5min7"),
    ("VII",     "G#5min7b5"),
])
def test_harmony_parse_degree(degree_name, expected_chord):
    harmony = Harmony(Scale("A4", "major"))

    assert harmony.get(degree_name, strict=False) == Chord.get_from_fullname(expected_chord)


@mark.parametrize("degree_name,expected_chord", [
    ("i",       "A4min7"),
    ("I",       "A4maj7"),
    ("ii",      "B4min7"),
    ("II",      "B4min7"),
    ("bII",     "Bb4min7"),
    ("IV",      "D5maj7"),
    ("bIV",     "Db5maj7"),
    ("#V",      "E#57"),
    ("VI7",     "F#57"),
    ("VIIdim7", "G#5dim7"),
    ("vii",     "G#5min7b5"),
    ("viimin7", "G#5min7"),
    ("VII",     "G#5min7b5"),
])
def test_harmony_parse_degree_non_strictly(degree_name, expected_chord):
    harmony = Harmony(Scale("A4", "major"))

    assert harmony.get(degree_name, strict=False) == Chord.get_from_fullname(expected_chord)
