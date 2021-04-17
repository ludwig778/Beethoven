from pytest import mark

from beethoven.repository.midi import MidiRepository
from beethoven.sequencer.grid import Grid
from beethoven.sequencer.jam_room import JamRoom
from tests.fixtures.fake_players import FakePlayer1, FakePlayer2


@mark.parametrize("harmony_str,players,expected_messages,expected_length", [
    # Test with empty harmony string
    (
        "",
        [FakePlayer1()],
        [
            {"type": "end_of_track", "time": 0}
        ],
        0.0
    ),
    # Test with empty harmony string
    (
        "n=A ts=4/4 sc=major t=60 p=",
        [FakePlayer1()],
        [
            {"type": "end_of_track", "time": 0}
        ],
        0.0
    ),
    # Basic test with no players
    (
        "n=A ts=4/4 sc=major t=60 p=I",
        [],
        [
            {"type": "text", "text": "1", "time": 0},
            {"type": "end_of_track", "time": 4.166666666666667}
        ],
        4.0
    ),
    # Basic test
    (
        "n=A ts=4/4 sc=major t=60 p=I",
        [FakePlayer1()],
        [
            {"type": "text",     "text": "1", "time": 0},
            {"type": "note_on",  "note": 69, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 73, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_off", "note": 69, "velocity": 127, "channel": 0, "time": 4.166666666666667},
            {"type": "note_off", "note": 73, "velocity": 127, "channel": 0, "time": 0},
            {"type": "end_of_track", "time": 0}
        ],
        4.0
    ),
    # Testing duration to grid part
    (
        "n=A ts=4/4 sc=major t=60 p=I:d=H",
        [FakePlayer1()],
        [
            {"type": "text",     "text": "1", "time": 0},
            {"type": "note_on",  "note": 69, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 73, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_off", "note": 69, "velocity": 127, "channel": 0, "time": 2.0833333333333335},
            {"type": "note_off", "note": 73, "velocity": 127, "channel": 0, "time": 0},
            {"type": "end_of_track", "time": 0}
        ],
        2.0
    ),
    # Testing duration to grid part with multiplier
    (
        "n=A ts=4/4 sc=major t=60 p=I:d=2Q",
        [FakePlayer1()],
        [
            {"type": "text",     "text": "1", "time": 0},
            {"type": "note_on",  "note": 69, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 73, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_off", "note": 69, "velocity": 127, "channel": 0, "time": 2.0833333333333335},
            {"type": "note_off", "note": 73, "velocity": 127, "channel": 0, "time": 0},
            {"type": "end_of_track", "time": 0}
        ],
        2.0
    ),
    # Testing duration with time signature fill
    (
        "n=A ts=4/4 sc=major t=60 p=I:d=Q,II",
        [FakePlayer1()],
        [
            {"type": "text",     "text": "1", "time": 0},
            {"type": "note_on",  "note": 69, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 73, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_off", "note": 69, "velocity": 127, "channel": 0, "time": 1.0416666666666667},
            {"type": "note_off", "note": 73, "velocity": 127, "channel": 0, "time": 0},
            {"type": "text",     "text": "2", "time": 0},
            {"type": "note_on",  "note": 71, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 75, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_off", "note": 71, "velocity": 127, "channel": 0, "time": 3.125},
            {"type": "note_off", "note": 75, "velocity": 127, "channel": 0, "time": 0},
            {"type": "end_of_track", "time": 0}
        ],
        4.0
    ),
    # Testing duration with time signature fill with another duration
    (
        "n=A ts=4/4 sc=major t=60 p=I:d=Q,II,III:d=3Q",
        [FakePlayer1()],
        [
            {"type": "text",     "text": "1", "time": 0},
            {"type": "note_on",  "note": 69, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 73, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_off", "note": 69, "velocity": 127, "channel": 0, "time": 1.0416666666666667},
            {"type": "note_off", "note": 73, "velocity": 127, "channel": 0, "time": 0},
            {"type": "text",     "text": "2", "time": 0},
            {"type": "note_on",  "note": 71, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 75, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_off", "note": 71, "velocity": 127, "channel": 0, "time": 3.125},
            {"type": "note_off", "note": 75, "velocity": 127, "channel": 0, "time": 0},
            {"type": "text",     "text": "3", "time": 0},
            {"type": "note_on",  "note": 61, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 65, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_off", "note": 61, "velocity": 127, "channel": 0, "time": 3.125},
            {"type": "note_off", "note": 65, "velocity": 127, "channel": 0, "time": 0},
            {"type": "end_of_track", "time": 0}
        ],
        7.0
    ),
    # Testing duration with time signature fill
    (
        "n=A ts=4/4 sc=major t=60 p=I:d=Q,II,III:d=3Q",
        [FakePlayer1()],
        [
            {"type": "text",     "text": "1", "time": 0},
            {"type": "note_on",  "note": 69, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 73, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_off", "note": 69, "velocity": 127, "channel": 0, "time": 1.0416666666666667},
            {"type": "note_off", "note": 73, "velocity": 127, "channel": 0, "time": 0},
            {"type": "text",     "text": "2", "time": 0},
            {"type": "note_on",  "note": 71, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 75, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_off", "note": 71, "velocity": 127, "channel": 0, "time": 3.125},
            {"type": "note_off", "note": 75, "velocity": 127, "channel": 0, "time": 0},
            {"type": "text",     "text": "3", "time": 0},
            {"type": "note_on",  "note": 61, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 65, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_off", "note": 61, "velocity": 127, "channel": 0, "time": 3.125},
            {"type": "note_off", "note": 65, "velocity": 127, "channel": 0, "time": 0},
            {"type": "end_of_track", "time": 0}
        ],
        7.0
    ),
    # Testing with split/spanned duration over time signatures
    (
        "n=A ts=4/4 sc=major t=60 p=I:d=Q,II:d=W,III",
        [FakePlayer1()],
        [
            {"type": "text",     "text": "1", "time": 0},
            {"type": "note_on",  "note": 69, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 73, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_off", "note": 69, "velocity": 127, "channel": 0, "time": 1.0416666666666667},
            {"type": "note_off", "note": 73, "velocity": 127, "channel": 0, "time": 0},
            {"type": "text",     "text": "2", "time": 0},
            {"type": "note_on",  "note": 71, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 75, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_off", "note": 71, "velocity": 127, "channel": 0, "time": 4.166666666666667},
            {"type": "note_off", "note": 75, "velocity": 127, "channel": 0, "time": 0},
            {"type": "text",     "text": "3", "time": 0},
            {"type": "note_on",  "note": 61, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 65, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_off", "note": 61, "velocity": 127, "channel": 0, "time": 3.125},
            {"type": "note_off", "note": 65, "velocity": 127, "channel": 0, "time": 0},
            {"type": "end_of_track", "time": 0}
        ],
        8.0
    ),
    # Basic test with multiple players
    (
        "n=A ts=4/4 sc=major t=60 p=I",
        [FakePlayer1(), FakePlayer2()],
        [
            {"type": "text",     "text": "1", "time": 0},
            {"type": "note_on",  "note": 69, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 73, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 62, "velocity": 63,  "channel": 1, "time": 0},
            {"type": "note_off", "note": 62, "velocity": 127, "channel": 1, "time": 2.0833333333333335},
            {"type": "note_on",  "note": 62, "velocity": 63,  "channel": 1, "time": 0},
            {"type": "note_off", "note": 69, "velocity": 127, "channel": 0, "time": 2.0833333333333335},
            {"type": "note_off", "note": 73, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_off", "note": 62, "velocity": 127, "channel": 1, "time": 0},
            {"type": "end_of_track", "time": 0}
        ],
        4.0
    ),
    # Test with time signature change
    (
        "n=A ts=4/4 sc=major t=60 p=I;ts=2/2 p=II",
        [FakePlayer1()],
        [
            {"type": "text",     "text": "1", "time": 0},
            {"type": "note_on",  "note": 69, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 73, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_off", "note": 69, "velocity": 127, "channel": 0, "time": 4.166666666666667},
            {"type": "note_off", "note": 73, "velocity": 127, "channel": 0, "time": 0},
            {"type": "text",     "text": "2", "time": 0},
            {"type": "note_on",  "note": 71, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 75, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_off", "note": 71, "velocity": 127, "channel": 0, "time": 4.166666666666667},
            {"type": "note_off", "note": 75, "velocity": 127, "channel": 0, "time": 0},
            {"type": "end_of_track", "time": 0}
        ],
        8.0
    ),
])
def test_midi_messages_from_jam_room(harmony_str, players, expected_messages, expected_length, monkeypatch):
    midi = MidiRepository(virtual=True)

    room = JamRoom(
        grid=Grid.parse(harmony_str),
        players=players
    )

    def get_messages(midi_file, **kwargs):
        messages = []

        for msg in midi_file:
            if msg.type == "text":
                messages.append(msg.__dict__)

            elif msg.type == "end_of_track":
                messages.append({"type": msg.type, "time": msg.time})

            else:
                messages.append({
                    "type": msg.type,
                    "channel": msg.channel,
                    "note": msg.note,
                    "velocity": msg.velocity,
                    "time": msg.time
                })

        return messages

    midi_file = midi._generate_midi_file(room.grid, room.players)
    messages = get_messages(midi_file)

    assert messages == expected_messages
    assert midi_file.length == expected_length * 1.0416666666666667
