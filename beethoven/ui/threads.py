from pprint import pprint
from time import sleep
from typing import Dict, List

from PySide6.QtCore import QThread, SignalInstance

from beethoven import controllers
from beethoven.adapters.midi import Input, MidiAdapter
from beethoven.models import Grid, Note
from beethoven.sequencer.players.base import BasePlayer
from beethoven.sequencer.playroom import play_grid
from beethoven.ui.settings import AppSettings


class TestThread(QThread):
    def __init__(self, *args, settings: AppSettings, **kwargs):
        super(TestThread, self).__init__(*args, **kwargs)
        self.settings = settings

    def run(self, *args, **kwargs):
        while 1:
            # os.system('clear')
            print("THREAD RUNNING", args, kwargs)
            pprint(self.settings.dict())
            sleep(4)


class MidiInputThread(QThread):
    def __init__(
        self, *args, midi_input: Input, note_changed_signal: SignalInstance, **kwargs
    ):
        super(MidiInputThread, self).__init__(*args, **kwargs)

        self.midi_input = midi_input
        self.note_changed_signal = note_changed_signal

    def run(self):
        midi_notes: Dict[int, Note] = dict()

        for message in self.midi_input:
            if message.type not in ("note_on", "note_off"):
                continue

            note = controllers.note.from_midi_index(message.note)

            if message.type == "note_on":
                midi_notes[message.note] = note

            if message.type == "note_off":
                if message.note in midi_notes:
                    del midi_notes[message.note]

            self.note_changed_signal.emit(midi_notes)


class MidiOutputThread(QThread):
    def __init__(
        self,
        *args,
        midi_adapter: MidiAdapter,
        players: List[BasePlayer],
        grid: Grid,
        **kwargs
    ):
        super(MidiOutputThread, self).__init__()  # *args, **kwargs)

        self.midi_adapter = midi_adapter
        self.players = players
        self.grid = grid

    def run(self):
        play_grid(
            self.midi_adapter,
            self.players,
            self.grid,
        )
        print("END")

    def clean(self):
        print("CLEAN")
        self.midi_adapter.reset()
