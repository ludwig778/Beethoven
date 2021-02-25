from beethoven.sequencer.note import Note
from beethoven.sequencer.note_duration import Whole
from beethoven.sequencer.players.base import BasePlayer
from beethoven.sequencer.time_signature import TimeContainer


class FakePlayer(BasePlayer):
    NOTE_DURATION = Whole


def test_base_player_capabilities():
    player = FakePlayer()

    assert repr(player) == "<Player FakePlayer>"

    assert player.play(TimeContainer(1, 1, 1), "F4", "F5", velocity=63) == {
        "part": TimeContainer(1, 1, 1),
        "notes": [Note("F4"), Note("F5")],
        "duration": Whole,
        "velocity": 63
    }
