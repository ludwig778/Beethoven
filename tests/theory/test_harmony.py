from pytest import mark, raises

from beethoven.theory.chord import Chord
from beethoven.theory.harmony import Harmony
from beethoven.theory.scale import Scale


@mark.parametrize("scale_name", [
    ("ionian"),
    ("melodic minor"),
    ("harmonic minor"),
    ("double harmonic minor"),
    ("lydian")
])
def test_harmony_instanciation_on_diatonic_scale(scale_name):
    Harmony(Scale("A", scale_name))


def test_harmony_instanciation_without_attributes():
    with raises(ValueError, match="Scale must be set"):
        Harmony()


def test_harmony_instanciation_through_to_dict():
    harmony = Harmony(Scale("A", "major"))

    assert harmony == Harmony(**harmony.to_dict())


@mark.parametrize("scale_name", [
    ("bebop"),
    ("chromatic"),
    ("pentatonic"),
    ("blues major"),
])
def test_harmony_instanciation_on_non_diatonic_scale(scale_name):
    with raises(ValueError, match="Scale given to harmony must be diatonic"):
        Harmony(Scale("A", scale_name))


def test_harmony_repr():
    assert repr(Harmony(Scale("A", "ionian"))) == "<Harmony A ionian>"


@mark.parametrize("degree_name,expected_chord", [
    ("I",       "Amaj7"),
    ("ii",      "Bmin7"),
    ("II",      "Bmaj7"),
    ("bII",     "Bbmaj7"),
    ("IV",      "Dmaj7"),
    ("bIV",     "Dbmaj7"),
    ("#V",      "E#7"),
    ("VI7",     "F#7"),
    ("VIIdim7", "G#dim7"),
    ("vii",     "G#min7b5"),
    ("viimin7", "G#min7"),
    ("VII",     "G#maj7"),
])
def test_harmony_parse_degree(degree_name, expected_chord):
    harmony = Harmony(Scale("A", "major"))

    assert harmony.get(degree_name) == Chord.get_from_fullname(expected_chord)


@mark.parametrize("scale_name,expected_degrees", [
    ("ionian",                "I,ii,iii,IV,V,vi,vii"),
    ("melodic minor",         "i,ii,III,IV,V,vi,vii"),
    ("harmonic minor",        "i,ii,III,iv,V,VI,vii"),
    ("double harmonic minor", "I,II,iii,iv,V,VI,vii"),
    ("lydian",                "I,II,iii,iv,V,vi,vii"),
    ("mixolydian",            "I,ii,iii,IV,v,vi,VII"),
    ("aeolian",               "i,ii,III,iv,v,VI,VII")
])
def test_harmony_degrees_and_notes(scale_name, expected_degrees):
    harmony = Harmony(Scale("A", scale_name))

    assert harmony.degrees == expected_degrees.split(",")


def test_harmony_degrees_and_noteslmao():
    harmony = Harmony(Scale("A", "ionian"))

    assert harmony.get("i", seventh=False) == Chord.get_from_fullname("Amin")
    assert harmony.get("II", seventh=False) == Chord.get_from_fullname("Bmaj")
