import logging
from typing import List

from PySide6.QtCore import QObject, Signal

from beethoven.adapters.midi import MidiAdapter
from beethoven.settings import AppSettings
from beethoven.ui.threads import MidiInputThread, MidiOutputThread

logger = logging.getLogger("manager.midi")


class MidiManager(QObject):
    input_notes_changed = Signal(dict)
    input_event_trigger = Signal(dict)

    def __init__(self, *args, settings: AppSettings, midi_adapter: MidiAdapter, **kwargs):
        super(MidiManager, self).__init__(*args, **kwargs)

        self.settings = settings
        self.midi_adapter = midi_adapter

        self.input_thread: MidiInputThread | None = None
        self.output_thread: MidiOutputThread | None = None

        if self.settings.midi.opened_outputs:
            self.update_outputs(self.settings.midi.opened_outputs)

        if self.settings.midi.selected_input:
            self.update_input(self.settings.midi.selected_input)

    def update_input(self, input_name: str):
        logger.info(f"input set to: {input_name or 'none'}")

        if self.input_thread and (not input_name or input_name != self.input_thread.midi_input.name):
            self.midi_adapter.close_input(self.input_thread.midi_input)

            self.terminate_input_thread()

        if not input_name:
            return

        midi_input = self.midi_adapter.open_input(input_name)

        if midi_input:
            self.current_input = input_name

            self.input_thread = MidiInputThread(
                midi_input=midi_input,
                on_note_change=self.input_notes_changed,
                on_event_trigger=self.input_event_trigger
            )
            self.input_thread.start()

    def update_outputs(self, output_names: List[str]):
        print("update_outputs")
        logger.info(f"outputs set to: {', '.join(output_names) or 'none'}")

        for output_name in output_names:
            self.midi_adapter.open_output(output_name)

        # ????
        # if self.input_thread:
        #     self.input_thread.terminate()

    def clean(self):
        self.midi_adapter.reset()

    def terminate_input_thread(self):
        if self.input_thread:
            self.input_thread.terminate()
            self.input_thread.wait()
            self.input_thread = None

    def terminate_output_thread(self):
        self.clean()

        if self.output_thread:
            self.output_thread.finished.disconnect()
            self.output_thread.terminate()
            self.output_thread.wait()
            self.output_thread = None

    def terminate_threads(self):
        self.terminate_input_thread()
        self.terminate_output_thread()
