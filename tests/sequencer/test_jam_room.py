from pytest import mark

from beethoven.repository.midi import midi
from beethoven.sequencer.grid import Grid
from beethoven.sequencer.jam_room import JamRoom
from beethoven.sequencer.note import Note
from tests.fixtures.fake_players import FakePlayer1, FakePlayer2


@mark.parametrize("harmony_str,players,expected_timeline,expected_length", [
    # Test with empty harmony string
    (
        "",
        [FakePlayer1()],
        {},
        0.0
    ),
    # Test with empty harmony string
    (
        "n=A ts=4/4 sc=major t=60 p=",
        [FakePlayer1()],
        {},
        0.0
    ),
    # Basic test with no players
    (
        "n=A ts=4/4 sc=major t=60 p=I",
        [],
        {},
        4.0
    ),
    # Basic test
    (
        "n=A ts=4/4 sc=major t=60 p=I",
        [FakePlayer1()],
        {
            0.0: [
                {
                    'channel': 0,
                    'duration': 4.0,
                    'notes': (Note("A3"), Note("C#4")),
                    'velocity': 127
                }
            ]
        },
        4.0
    ),
    # Testing duration to grid part
    (
        "n=A ts=4/4 sc=major t=60 p=I:H",
        [FakePlayer1()],
        {
            0.0: [
                {
                    'channel': 0,
                    'duration': 2.0,
                    'notes': (Note("A3"), Note("C#4")),
                    'velocity': 127
                }
            ]
        },
        2.0
    ),
    # Testing duration to grid part with multiplier
    (
        "n=A ts=4/4 sc=major t=60 p=I:2Q",
        [FakePlayer1()],
        {
            0.0: [
                {
                    'channel': 0,
                    'duration': 2.0,
                    'notes': (Note("A3"), Note("C#4")),
                    'velocity': 127
                }
            ]
        },
        2.0
    ),
    # Testing duration with time signature fill
    (
        "n=A ts=4/4 sc=major t=60 p=I:Q,II",
        [FakePlayer1()],
        {
            0.0: [
                {
                    'channel': 0,
                    'duration': 1.0,
                    'notes': (Note("A3"), Note("C#4")),
                    'velocity': 127
                }
            ],
            1.0: [
                {
                    'channel': 0,
                    'duration': 3.0,
                    'notes': (Note("B3"), Note("D#4")),
                    'velocity': 127
                }
            ]
        },
        4.0
    ),
    # Testing duration with time signature fill with another duration
    (
        "n=A ts=4/4 sc=major t=60 p=I:Q,II,III:3Q",
        [FakePlayer1()],
        {
            0.0: [
                {
                    'channel': 0,
                    'duration': 1.0,
                    'notes': (Note("A3"), Note("C#4")),
                    'velocity': 127
                }
            ],
            1.0: [
                {
                    'channel': 0,
                    'duration': 3.0,
                    'notes': (Note("B3"), Note("D#4")),
                    'velocity': 127
                }
            ],
            4.0: [
                {
                    'channel': 0,
                    'duration': 3.0,
                    'notes': (Note("C#3"), Note("E#3")),
                    'velocity': 127
                }
            ]
        },
        7.0
    ),
    # Testing duration with time signature fill
    (
        "n=A ts=4/4 sc=major t=60 p=I:Q,II,III:3Q",
        [FakePlayer1()],
        {
            0.0: [
                {
                    'channel': 0,
                    'duration': 1.0,
                    'notes': (Note("A3"), Note("C#4")),
                    'velocity': 127
                }
            ],
            1.0: [
                {
                    'channel': 0,
                    'duration': 3.0,
                    'notes': (Note("B3"), Note("D#4")),
                    'velocity': 127
                }
            ],
            4.0: [
                {
                    'channel': 0,
                    'duration': 3.0,
                    'notes': (Note("C#3"), Note("E#3")),
                    'velocity': 127
                }
            ]
        },
        7.0
    ),
    # Testing with split/spanned duration over time signatures
    (
        "n=A ts=4/4 sc=major t=60 p=I:Q,II:W,III",
        [FakePlayer1()],
        {
            0.0: [
                {
                    'channel': 0,
                    'duration': 1.0,
                    'notes': (Note("A3"), Note("C#4")),
                    'velocity': 127
                }
            ],
            1.0: [
                {
                    'channel': 0,
                    'duration': 4.0,
                    'notes': (Note("B3"), Note("D#4")),
                    'velocity': 127
                }
            ],
            5.0: [
                {
                    'channel': 0,
                    'duration': 3.0,
                    'notes': (Note("C#3"), Note("E#3")),
                    'velocity': 127
                }
            ]
        },
        8.0
    ),
    # Basic test with multiple players
    (
        "n=A ts=4/4 sc=major t=60 p=I",
        [FakePlayer1(), FakePlayer2()],
        {
            0.0: [
                {
                    'channel': 0,
                    'duration': 4.0,
                    'notes': (Note("A3"), Note("C#4")),
                    'velocity': 127
                },
                {
                    'channel': 1,
                    'duration': 2.0,
                    'notes': (Note("D3"),),
                    'velocity': 63
                }
            ],
            2.0: [
                {
                    'channel': 1,
                    'duration': 2.0,
                    'notes': (Note("D3"),),
                    'velocity': 63
                }
            ]
        },
        4.0
    ),
    # Test with time signature change
    (
        "n=A ts=4/4 sc=major t=60 p=I;ts=2/2 p=II",
        [FakePlayer1()],
        {
            0.0: [
                {
                    'channel': 0,
                    'duration': 4.0,
                    'notes': (Note("A3"), Note("C#4")),
                    'velocity': 127
                }
            ],
            4.0: [
                {
                    'channel': 0,
                    'duration': 4.0,
                    'notes': (Note("B3"), Note("D#4")),
                    'velocity': 127
                }
            ]
        },
        8.0
    ),
])
def test_create_jam_room(harmony_str, players, expected_timeline, expected_length):
    room = JamRoom(
        grid=Grid.parse(harmony_str),
        players=players
    )

    assert room.timeline == expected_timeline
    assert room.length == expected_length


def test_jam_room_play(monkeypatch):
    def mock_midi_play(timeline, length, **kwargs):
        return timeline, length, kwargs

    monkeypatch.setattr(midi, "play", mock_midi_play)

    room = JamRoom(
        grid=Grid.parse("n=A sc=major p=I"),
        players=[FakePlayer1()]
    )

    assert room.play() == (
        {
            0.0: [
                {
                    'channel': 0,
                    'duration': 4.0,
                    'notes': (Note("A3"), Note("C#4")),
                    'velocity': 127
                },
            ]
        },
        4.0,
        {}
    )
