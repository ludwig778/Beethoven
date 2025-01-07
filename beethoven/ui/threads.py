import logging
from typing import Dict

from PySide6.QtCore import QThread, SignalInstance

from beethoven.adapters.midi import Input, MidiAdapter, MidiControlMessage
from beethoven.models import Note
from beethoven.sequencer.runner import Sequencer


class MidiInputThread(QThread):
    def __init__(
        self,
        midi_input: Input,
        on_note_change: SignalInstance,
        on_event_trigger: SignalInstance,
    ):
        super(MidiInputThread, self).__init__()

        self.logger = logging.getLogger("threads.midi_input")

        self.midi_input = midi_input
        self.on_note_change = on_note_change
        self.on_event_trigger = on_event_trigger

    def run(self):
        midi_notes: Dict[int, Note] = dict()
        print("RUN")

        for message in self.midi_input:
            if message.type == "control_change":
                self.on_event_trigger.emit(MidiControlMessage(
                    input=self.midi_input,
                    type=message.type,
                    channel=message.channel,
                    control=message.control,
                    value=message.value,
                ))

                continue
            elif message.type not in ("note_on", "note_off"):
                continue

            note = Note.from_midi_index(message.note)

            if message.type == "note_on":
                midi_notes[message.note] = note
                print("RUN", [message.note, note])

            if message.type == "note_off":
                if message.note in midi_notes:
                    del midi_notes[message.note]

            self.on_note_change.emit(midi_notes)


class MidiOutputThread(QThread):
    def __init__(
        self,
        midi_adapter: MidiAdapter,
        sequencer: Sequencer,
    ):
        super(MidiOutputThread, self).__init__()

        self.logger = logging.getLogger("threads.midi_output")

        self.midi_adapter = midi_adapter
        self.sequencer = sequencer

    def run(self):
        self.logger.info("run start")

        self.sequencer.run()

    def clean(self):
        self.logger.info("clean midi output")

        self.midi_adapter.reset()
