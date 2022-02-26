from typing import Dict, Union

from mido import Message, MetaMessage, open_output
from mido.backends.rtmidi import Output
from pydantic import BaseModel


class MidiMessage(BaseModel):
    note: int
    output: Output
    channel: int
    velocity: int
    type: str

    def to_mido(self) -> Message:
        return Message(
            self.type, note=self.note, channel=self.channel, velocity=self.velocity
        )

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
outputs: Dict[str, Output] = {}


class MidiAdapter:
    def __init__(self) -> None:
        self.outputs = outputs

    def open_output(self, name: str) -> Output:
        output = self.outputs.get(name)

        if not output:
            output = open_output(name, virtual=True)
            self.outputs[name] = output

        return output

    def close_output(self, name: str) -> None:
        if name in self.outputs:
            self.outputs[name].close()

            del self.outputs[name]

    def close_all_outputs(self) -> None:
        for name in list(self.outputs):
            self.close_output(name)

    def send_message(self, message: MidiMessageType) -> None:
        if message.type == "text":
            message.output._send(message.to_mido())
        else:
            message.output.send(message.to_mido())

    def shutdown(self) -> None:
        for output in self.outputs.values():
            output.panic()
