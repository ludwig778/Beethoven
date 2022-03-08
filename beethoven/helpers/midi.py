from time import sleep
from typing import Tuple

from beethoven.adapters.midi import MidiMessage, Output
from beethoven.models import Duration
from beethoven.types import NotesContainer


def get_on_off_messages(
    note_index: int, output: Output, channel: int, velocity: int = 127
) -> Tuple[MidiMessage, MidiMessage]:
    midi_message_kwargs = {
        "note": note_index,
        "output": output,
        "channel": channel,
        "velocity": velocity,
    }

    return (
        MidiMessage(type="note_on", **midi_message_kwargs),
        MidiMessage(type="note_off", **midi_message_kwargs),
    )


def play_note(
    note_index: int,
    output: Output,
    channel: int,
    velocity: int = 127,
    duration: Duration = Duration(value=1),
) -> None:
    note_on, note_off = get_on_off_messages(
        note_index, output, channel, velocity=velocity
    )

    output.send(note_on.to_mido())

    sleep(float(duration.value))

    output.send(note_off.to_mido())


def play_notes(
    notes_container: NotesContainer,
    output: Output,
    channel: int,
    velocity: int = 127,
    duration: Duration = Duration(value=1),
) -> None:
    notes_on = []
    notes_off = []

    for note in notes_container.notes:
        note_on, note_off = get_on_off_messages(
            note.midi_index, output, channel, velocity=velocity
        )

        notes_on.append(note_on)
        notes_off.append(note_off)

    for note_on in notes_on:
        output.send(note_on.to_mido())

    sleep(float(duration.value))

    for note_off in notes_off:
        output.send(note_off.to_mido())
