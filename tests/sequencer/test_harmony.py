from pytest import mark, raises

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


@mark.parametrize("degree_name", [
    ("I"),
    ("ii"),
    ("II"),
    ("bII"),
    ("IV"),
    ("bIV"),
    ("V"),
    ("VI7"),
    ("VIIdim7"),
    ("vii"),
    ("#VII"),
])
def test_harmony_parse_degree(degree_name):
    harmony = Harmony(Scale("E4", "major"))

    harmony.get(degree_name)
