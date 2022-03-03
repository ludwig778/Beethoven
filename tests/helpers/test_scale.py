from beethoven.helpers.scale import get_diatonic_scale_chords
from tests.fixtures.scales import c_major, c_major_7th_chords


def test_scale_helper_get_diatonic_scale_chords():
    assert get_diatonic_scale_chords(c_major) == c_major_7th_chords
