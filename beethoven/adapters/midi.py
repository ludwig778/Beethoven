from typing import Dict, Union

from mido import Message, MetaMessage, get_input_names, open_input, open_output
from mido.backends.rtmidi import Input, Output
from pydantic import BaseModel


class MidiMessage(BaseModel):
    note: int
    output: Output
    channel: int
    velocity: int
    type: str

    def to_mido(self) -> Message:
        return Message(self.type, note=self.note, channel=self.channel, velocity=self.velocity)

    class Config:
        arbitrary_types_allowed = True


class MidiMetaMessage(BaseModel):
    output: Output
    type: str
    text: str

    def to_mido(self) -> MetaMessage:
        return MetaMessage(self.type, text=self.text)

    class Config:
        arbitrary_types_allowed = True


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
