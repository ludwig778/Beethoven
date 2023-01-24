from logging import getLogger
from pprint import pprint
from time import sleep
from typing import Callable, Dict, List, Optional

from PySide6.QtCore import QThread, SignalInstance

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
        self, *args, midi_input: Input, on_note_change: SignalInstance, **kwargs
    ):
        super(MidiInputThread, self).__init__(*args, **kwargs)

        self.logger = getLogger("threads.midi_input")

        self.midi_input = midi_input
        self.on_note_change = on_note_change

    def run(self):
        midi_notes: Dict[int, Note] = dict()

        for message in self.midi_input:
            if message.type not in ("note_on", "note_off"):
                continue

            note = Note.from_midi_index(message.note)

            if message.type == "note_on":
                midi_notes[message.note] = note

            if message.type == "note_off":
                if message.note in midi_notes:
                    del midi_notes[message.note]

            self.on_note_change.emit(midi_notes)


class MidiOutputThread(QThread):
    def __init__(
        self,
        *args,
        midi_adapter: MidiAdapter,
        players: List[BasePlayer],
        grid: Grid,
        on_grid_part_change: Optional[Callable] = None,
        on_grid_part_end: Optional[Callable] = None,
        **kwargs
    ):
        super(MidiOutputThread, self).__init__()  # *args, **kwargs)

        self.logger = getLogger("threads.midi_output")

        self.midi_adapter = midi_adapter
        self.players = players
        self.grid = grid
        self.on_grid_part_change = on_grid_part_change

        self.finished.connect(on_grid_part_end)

    def run(self):
        self.logger.info("run start")
        play_grid(self.midi_adapter, self.players, self.grid, self.on_grid_part_change)

    def clean(self):
        self.logger.info("clean midi output")

        self.midi_adapter.reset()
