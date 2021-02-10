from pytest import mark

from beethoven.sequencer.interval import Interval
from beethoven.sequencer.note import Note


@mark.parametrize("start_note,interval_name,expected_note", [
    ("A4", "2m", "Bb4"),
    ("B5", "9a", "C##7"),
    ("G4", "13M", "E6"),
    ("C4", "4a", "F#4"),
    ("D4", "7d", "Cb5")
])
def test_interval_check_display(start_note, interval_name, expected_note):
    assert Note(start_note) + Interval(interval_name) == Note(expected_note)
