from pytest import mark

from beethoven.repository.midi import MidiRepository
from beethoven.theory.scale import Scale
from beethoven.theory.chord import Chord
from beethoven.sequencer.grid import Grid, GridPart
from beethoven.sequencer.jam_room import JamRoom
from beethoven.sequencer.note_duration import Whole, Half, Quarter
from beethoven.sequencer.tempo import Tempo
from beethoven.sequencer.time_signature import TimeSignature
from tests.fixtures.fake_players import FakePlayer1, FakePlayer2


@mark.parametrize("grid,players,expected_messages,expected_length", [
    # Test with empty grid
    (
        Grid(),
        [FakePlayer1()],
        [
            {"type": "end_of_track", "time": 0}
        ],
        0.0
    ),
    # Basic test with no players
    (
        Grid([
            GridPart(
                scale=Scale("A", "major"),
                chord=Chord("A", "maj"),
                tempo=Tempo(60),
                duration=None,
                time_signature=TimeSignature(4, 4)
            )
        ]),
        [],
        [
            {"type": "text", "text": "1", "time": 0},
            {"type": "end_of_track", "time": 4.166666666666667}
        ],
        4.0
    ),
    # Basic test
    (
        Grid([
            GridPart(
                scale=Scale("A", "major"),
                chord=Chord("A", "maj"),
                tempo=Tempo(60),
                duration=None,
                time_signature=TimeSignature(4, 4)
            )
        ]),
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
        Grid([
            GridPart(
                scale=Scale("A", "major"),
                chord=Chord("A", "maj"),
                tempo=Tempo(60),
                duration=Half,
                time_signature=TimeSignature(4, 4)
            )
        ]),
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
        Grid([
            GridPart(
                scale=Scale("A", "major"),
                chord=Chord("A", "maj"),
                tempo=Tempo(60),
                duration=Quarter,
                time_signature=TimeSignature(4, 4)
            ),
            GridPart(
                scale=Scale("A", "major"),
                chord=Chord("B", "min"),
                tempo=Tempo(60),
                duration=None,
                time_signature=TimeSignature(4, 4)
            )
        ]),
        [FakePlayer1()],
        [
            {"type": "text",     "text": "1", "time": 0},
            {"type": "note_on",  "note": 69, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 73, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_off", "note": 69, "velocity": 127, "channel": 0, "time": 1.0416666666666667},
            {"type": "note_off", "note": 73, "velocity": 127, "channel": 0, "time": 0},
            {"type": "text",     "text": "2", "time": 0},
            {"type": "note_on",  "note": 71, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 74, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_off", "note": 71, "velocity": 127, "channel": 0, "time": 3.125},
            {"type": "note_off", "note": 74, "velocity": 127, "channel": 0, "time": 0},
            {"type": "end_of_track", "time": 0}
        ],
        4.0
    ),
    # Testing duration with time signature fill with another duration
    (
        Grid([
            GridPart(
                scale=Scale("A", "major"),
                chord=Chord("A", "maj"),
                tempo=Tempo(60),
                duration=Quarter,
                time_signature=TimeSignature(4, 4)
            ),
            GridPart(
                scale=Scale("A", "major"),
                chord=Chord("B", "min"),
                tempo=Tempo(60),
                duration=None,
                time_signature=TimeSignature(4, 4)
            ),
            GridPart(
                scale=Scale("A", "major"),
                chord=Chord("C#", "min"),
                tempo=Tempo(60),
                duration=Quarter * 3,
                time_signature=TimeSignature(4, 4)
            ),
        ]),
        [FakePlayer1()],
        [
            {"type": "text",     "text": "1", "time": 0},
            {"type": "note_on",  "note": 69, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 73, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_off", "note": 69, "velocity": 127, "channel": 0, "time": 1.0416666666666667},
            {"type": "note_off", "note": 73, "velocity": 127, "channel": 0, "time": 0},
            {"type": "text",     "text": "2", "time": 0},
            {"type": "note_on",  "note": 71, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 74, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_off", "note": 71, "velocity": 127, "channel": 0, "time": 3.125},
            {"type": "note_off", "note": 74, "velocity": 127, "channel": 0, "time": 0},
            {"type": "text",     "text": "3", "time": 0},
            {"type": "note_on",  "note": 61, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 64, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_off", "note": 61, "velocity": 127, "channel": 0, "time": 3.125},
            {"type": "note_off", "note": 64, "velocity": 127, "channel": 0, "time": 0},
            {"type": "end_of_track", "time": 0}
        ],
        7.0
    ),
    # Testing with split/spanned duration over time signatures
    (
        Grid([
            GridPart(
                scale=Scale("A", "major"),
                chord=Chord("A", "maj"),
                tempo=Tempo(60),
                duration=Quarter,
                time_signature=TimeSignature(4, 4)
            ),
            GridPart(
                scale=Scale("A", "major"),
                chord=Chord("B", "min"),
                tempo=Tempo(60),
                duration=Whole,
                time_signature=TimeSignature(4, 4)
            ),
            GridPart(
                scale=Scale("A", "major"),
                chord=Chord("C#", "min"),
                tempo=Tempo(60),
                duration=None,
                time_signature=TimeSignature(4, 4)
            ),
        ]),
        [FakePlayer1()],
        [
            {"type": "text",     "text": "1", "time": 0},
            {"type": "note_on",  "note": 69, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 73, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_off", "note": 69, "velocity": 127, "channel": 0, "time": 1.0416666666666667},
            {"type": "note_off", "note": 73, "velocity": 127, "channel": 0, "time": 0},
            {"type": "text",     "text": "2", "time": 0},
            {"type": "note_on",  "note": 71, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 74, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_off", "note": 71, "velocity": 127, "channel": 0, "time": 4.166666666666667},
            {"type": "note_off", "note": 74, "velocity": 127, "channel": 0, "time": 0},
            {"type": "text",     "text": "3", "time": 0},
            {"type": "note_on",  "note": 61, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 64, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_off", "note": 61, "velocity": 127, "channel": 0, "time": 3.125},
            {"type": "note_off", "note": 64, "velocity": 127, "channel": 0, "time": 0},
            {"type": "end_of_track", "time": 0}
        ],
        8.0
    ),
    # Basic test with multiple players
    (
        Grid([
            GridPart(
                scale=Scale("A", "major"),
                chord=Chord("A", "maj"),
                tempo=Tempo(60),
                duration=None,
                time_signature=TimeSignature(4, 4)
            )
        ]),
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
        Grid([
            GridPart(
                scale=Scale("A", "major"),
                chord=Chord("A", "maj"),
                tempo=Tempo(60),
                duration=None,
                time_signature=TimeSignature(4, 4)
            ),
            GridPart(
                scale=Scale("A", "major"),
                chord=Chord("B", "min"),
                tempo=Tempo(60),
                duration=None,
                time_signature=TimeSignature(2, 2)
            )
        ]),
        [FakePlayer1()],
        [
            {"type": "text",     "text": "1", "time": 0},
            {"type": "note_on",  "note": 69, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 73, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_off", "note": 69, "velocity": 127, "channel": 0, "time": 4.166666666666667},
            {"type": "note_off", "note": 73, "velocity": 127, "channel": 0, "time": 0},
            {"type": "text",     "text": "2", "time": 0},
            {"type": "note_on",  "note": 71, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_on",  "note": 74, "velocity": 127, "channel": 0, "time": 0},
            {"type": "note_off", "note": 71, "velocity": 127, "channel": 0, "time": 4.166666666666667},
            {"type": "note_off", "note": 74, "velocity": 127, "channel": 0, "time": 0},
            {"type": "end_of_track", "time": 0}
        ],
        8.0
    ),
])
def test_midi_messages_from_jam_room(grid, players, expected_messages, expected_length, monkeypatch):
    midi = MidiRepository(virtual=True)

    room = JamRoom(grid=grid, players=players)

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
