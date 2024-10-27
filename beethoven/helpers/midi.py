"""
from time import sleep
from typing import List, Tuple

from beethoven.adapters.midi import MidiMessage, Output
from beethoven.models import Duration, Note

# from beethoven.sequencer.runner import Message as PlayerMessage

def get_on_off_messages(
    #message,
    message: PlayerMessage,
    #note_index: int,
    output: Output,
    #channel: int,
    #velocity: int = 127
) -> Tuple[MidiMessage, MidiMessage] | None:
    note_index = message.midi_index

        if not note_index:
        return None

    midi_message_kwargs = {
        "output": output,
        "channel": message.player.setting.channel,



        "note": note_index,
        "velocity": message.velocity,
        "player": message.player,
    }

    opener = MidiMessage(type="note_on", **midi_message_kwargs),

    return opener, MidiMessage(type="note_off", opener=opener, **midi_message_kwargs)
    #,
        #MidiMessage(type="note_on", **midi_message_kwargs),
    #)


def play_note(
    note_index: int,
    output: Output,
    channel: int,
    velocity: int = 127,
    duration: Duration = Duration.parse("1"),
) -> None:
    note_on, note_off = get_on_off_messages(note_index, output, channel, velocity=velocity)

    output.send(note_on.to_mido())

    sleep(float(duration.value))

    output.send(note_off.to_mido())


def play_notes(
    notes: List[Note],
    output: Output,
    channel: int,
    velocity: int = 127,
    duration: Duration = Duration.parse("1"),
) -> None:
    notes_on = []
    notes_off = []

    for note in notes:
        note_on, note_off = get_on_off_messages(note.midi_index, output, channel, velocity=velocity)

        notes_on.append(note_on)
        notes_off.append(note_off)

    for note_on in notes_on:
        output.send(note_on.to_mido())

    sleep(float(duration.value))

    for note_off in notes_off:
        output.send(note_off.to_mido())
"""
