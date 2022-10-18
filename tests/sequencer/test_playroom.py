from pytest import fixture

from beethoven.constants.duration import sixteenth_value
from beethoven.models import Bpm, Grid, GridPart, TimeSignature
from beethoven.models.duration import Duration
from beethoven.sequencer.players.base import BasePlayer, PercussionPlayer
from beethoven.sequencer.playroom import play_grid
from tests.fixtures.chords import c4_maj, c_maj7, d_min7, e_min7
from tests.fixtures.scales import a_minor, c_major


@fixture(scope="function", autouse=True)
def mock_midi_adapter(mock_midi_adapter):
    pass


class Piano(BasePlayer):
    def play(self):
        timeline = Duration(value=0)

        duration = Duration(value=2)

        while True:
            for note in self.grid_part.chord.notes:
                yield timeline, self.play_note(note.midi_index, duration=duration)

            timeline += duration


class Metronome(PercussionPlayer):
    def play(self):
        timeline = Duration(value=0)

        while True:
            yield timeline, self.play_note(23, duration=Duration(value=1))

            timeline += Duration(value=1)


def test_playroom(adapters, monkeypatch):
    sleep_call_params = []

    def get_sleep_call_params(time):
        sleep_call_params.append(time)

    midi_messages = []

    def get_midi_message_attributes(msg):
        midi_messages.append(
            {
                "note": msg.note,
                "type": msg.type,
                "output_name": msg.output.name,
                "output_channel": msg.channel,
                "velocity": msg.velocity,
            }
        )

    monkeypatch.setattr("beethoven.sequencer.playroom.sleep", get_sleep_call_params)
    monkeypatch.setattr(adapters.midi, "send_message", get_midi_message_attributes)

    bpm = Bpm(value=120)
    time_signatures = [
        TimeSignature(beats_per_bar=4, beat_unit=4),
        TimeSignature(beats_per_bar=3, beat_unit=2),
        TimeSignature(beats_per_bar=5, beat_unit=8),
    ]

    grid = Grid(
        parts=[
            GridPart(
                scale=c_major,
                chord=d_min7,
                bpm=bpm,
                time_signature=time_signatures[0],
                duration=Duration(value=sixteenth_value * 3),
            ),
            GridPart(
                scale=c_major,
                chord=c4_maj,
                bpm=bpm,
                time_signature=time_signatures[0],
            ),
            GridPart(
                scale=a_minor,
                chord=e_min7,
                bpm=bpm,
                time_signature=time_signatures[1],
            ),
            GridPart(
                scale=a_minor,
                chord=c_maj7,
                bpm=bpm,
                time_signature=time_signatures[2],
            ),
        ],
    )
    players = [
        Piano().setup_midi(output=adapters.midi.open_output("Chords"), channel=1),
        Metronome().setup_midi(
            output=adapters.midi.open_output("Percussion"), channel=2
        ),
    ]

    play_grid(adapters.midi, players, grid)

    assert sleep_call_params == [
        0.375,
        0.125,
        0.5,
        0.375,
        0.125,
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        0.25,
    ]

    assert midi_messages == [
        {
            "note": 23,
            "output_channel": 2,
            "output_name": "Percussion",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 2,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 5,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 9,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 0,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 2,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 5,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 9,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 0,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 48,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 52,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 55,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 23,
            "output_channel": 2,
            "output_name": "Percussion",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 23,
            "output_channel": 2,
            "output_name": "Percussion",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 23,
            "output_channel": 2,
            "output_name": "Percussion",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 23,
            "output_channel": 2,
            "output_name": "Percussion",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 48,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 52,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 55,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 48,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 52,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 55,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 23,
            "output_channel": 2,
            "output_name": "Percussion",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 23,
            "output_channel": 2,
            "output_name": "Percussion",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 23,
            "output_channel": 2,
            "output_name": "Percussion",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 48,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 52,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 55,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 23,
            "output_channel": 2,
            "output_name": "Percussion",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 4,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 7,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 11,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 2,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 23,
            "output_channel": 2,
            "output_name": "Percussion",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 23,
            "output_channel": 2,
            "output_name": "Percussion",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 23,
            "output_channel": 2,
            "output_name": "Percussion",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 23,
            "output_channel": 2,
            "output_name": "Percussion",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 4,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 7,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 11,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 2,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 4,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 7,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 11,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 2,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 23,
            "output_channel": 2,
            "output_name": "Percussion",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 23,
            "output_channel": 2,
            "output_name": "Percussion",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 23,
            "output_channel": 2,
            "output_name": "Percussion",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 23,
            "output_channel": 2,
            "output_name": "Percussion",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 4,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 7,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 11,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 2,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 4,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 7,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 11,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 2,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 23,
            "output_channel": 2,
            "output_name": "Percussion",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 23,
            "output_channel": 2,
            "output_name": "Percussion",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 23,
            "output_channel": 2,
            "output_name": "Percussion",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 4,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 7,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 11,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 2,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 23,
            "output_channel": 2,
            "output_name": "Percussion",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 0,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 4,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 7,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 11,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 23,
            "output_channel": 2,
            "output_name": "Percussion",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 23,
            "output_channel": 2,
            "output_name": "Percussion",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 23,
            "output_channel": 2,
            "output_name": "Percussion",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 23,
            "output_channel": 2,
            "output_name": "Percussion",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 0,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 4,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 7,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 11,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 0,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 4,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 7,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 11,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_on",
            "velocity": 127,
        },
        {
            "note": 23,
            "output_channel": 2,
            "output_name": "Percussion",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 0,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 4,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 7,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
        {
            "note": 11,
            "output_channel": 1,
            "output_name": "Chords",
            "type": "note_off",
            "velocity": 127,
        },
    ]
