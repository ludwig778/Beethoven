from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Dict, Protocol, Tuple, Union

from mido import Message, MetaMessage, get_input_names, open_input, open_output
from mido.backends.rtmidi import Input, Output

from beethoven.models import Duration, Note

#from beethoven.sequencer.players import Message as PlayerMessage

# from pydantic import BaseModel

class PlayerMessageProtocol(Protocol):
    note: Union[str, Note]
    player: Any
    velocity: int = 127
    duration: Duration = Duration()



@dataclass
class MidiMessage:
    origin: PlayerMessageProtocol
    output: Output
    channel: int
    velocity: int
    type: str
    note: int | None = None

    opener: MidiMessage | None = None

    def fix_note_midi_index(self):
        if isinstance(self.origin.note, str):
            if not self.origin.player.mapping:
                return False

            note = replace(self.origin.player.mapping.mappings.get(self.origin.note))

            if not isinstance(note, Note):
                return False
        else:
            note = self.origin.note

        self.note = note.midi_index

        return bool(self.note)

    def to_mido(self) -> Message:
        return Message(self.type, note=self.note, channel=self.channel, velocity=self.velocity)

    @classmethod
    def get_tuple_from_message(cls, message: PlayerMessageProtocol, output: Output) -> Tuple[MidiMessage, MidiMessage]:
        midi_message_kwargs = {
            # "note": message.note,
            "origin": message,
            "output": output,
            "channel": message.player.setting.channel,
            "velocity": message.velocity,
            # "player": message.player,
        }

        opener = MidiMessage(type="note_on", **midi_message_kwargs)

        return opener, MidiMessage(type="note_off", opener=opener, **midi_message_kwargs)
        # ,
        #     MidiMessage(type="note_on", **midi_message_kwargs),
        # )


@dataclass
class MidiMetaMessage:
    output: Output
    type: str
    text: str

    def to_mido(self) -> MetaMessage:
        return MetaMessage(self.type, text=self.text)


@dataclass
class MidiControlMessage:
    input: Input
    type: str
    channel: int
    control: int
    value: int
    # time: int

    # def to_mido(self) -> MetaMessage:
    #     return MetaMessage(self.type, text=self.text)


MidiMessageType = Union[MidiMessage, MidiMetaMessage]
Inputs = Dict[str, Input]
Outputs = Dict[str, Output]


class MidiAdapter:
    def __init__(self) -> None:
        self.inputs: Inputs = {}
        self.outputs: Outputs = {}

    def open_output(self, name: str) -> Output:
        output = self.outputs.get(name)

        if not output:
            output = open_output(name, virtual=True)
            self.outputs[name] = output

        return output

    @property
    def available_inputs(self):
        return get_input_names()

    def open_input(self, name: str) -> Input:
        input = self.inputs.get(name)

        if not input and name in self.available_inputs:
            input = open_input(name)
            self.inputs[name] = input

        return input

    def close_output(self, name: str) -> None:
        if name in self.outputs:
            self.outputs[name].close()

            del self.outputs[name]

    def close_input(self, name: str) -> None:
        if name in self.inputs:
            self.inputs[name].close()

            del self.inputs[name]

    def close_all_outputs(self) -> None:
        for name in list(self.outputs):
            self.close_output(name)

    def send_message(self, message: MidiMessageType) -> None:
        if message.type == "text":
            message.output._send(message.to_mido())
        else:
            message.output.send(message.to_mido())

    def reset(self) -> None:
        for output in self.outputs.values():
            output.reset()

    def shutdown(self) -> None:
        for output in self.outputs.values():
            output.panic()
