import logging
from enum import Enum, auto
from typing import Optional, Tuple

from PySide6.QtCore import QObject, QThread, Signal

from beethoven.adapters.factory import Adapters
from beethoven.models import ChordItem, HarmonyItem
from beethoven.sequencer.runner import Sequencer, SequencerParams
from beethoven.settings import AppSettings
from beethoven.ui.managers.midi import MidiManager
from beethoven.ui.threads import MidiOutputThread
from beethoven.ui.utils import setup_players

logger = logging.getLogger("manager.sequencer")


class SequencerState(Enum):
    playing = auto()
    playing_preview = auto()
    stopped = auto()


class SequencerManager(QObject):
    grid_play = Signal()
    grid_stop = Signal()
    grid_ended = Signal()

    items_change = Signal(HarmonyItem, ChordItem)

    def __init__(
        self,
        *args,
        settings: AppSettings,
        adapters: Adapters,
        midi_manager: MidiManager,
        **kwargs
    ):
        super(SequencerManager, self).__init__(*args, **kwargs)

        self.settings = settings
        self.adapters = adapters
        self.midi_manager = midi_manager

        self.sequencer = Sequencer(midi_adapter=self.adapters.midi)

        self.state = SequencerState.stopped

        self.grid_play.connect(self.play)
        self.grid_stop.connect(self.stop)

    def setup(self, params: SequencerParams):
        self.sequencer.params = params

    def is_playing(self) -> bool:
        return self.state == SequencerState.playing

    def is_playing_preview(self) -> bool:
        return self.state == SequencerState.playing_preview

    def is_stopped(self) -> bool:
        return self.state == SequencerState.stopped

    def play(self):
        logger.info("playing")

        if not self.is_stopped():
            self.midi_manager.terminate_output_thread()

        if self.sequencer.params.preview:
            self.state = SequencerState.playing_preview
        else:
            self.state = SequencerState.playing

        self.midi_manager.output_thread = MidiOutputThread(
            midi_adapter=self.adapters.midi, sequencer=self.sequencer
        )

        self.midi_manager.output_thread.start()
        self.midi_manager.output_thread.setPriority(QThread.TimeCriticalPriority)
        self.midi_manager.output_thread.finished.connect(self.finished)

    def get_players(self, preview: bool = False):
        if preview:
            player_settings = [self.settings.player.preview]
        else:
            player_settings = self.settings.player.players

        return setup_players(
            midi_adapter=self.adapters.midi, player_settings=player_settings
        )

    def get_current_items(self) -> Tuple[Optional[HarmonyItem], Optional[ChordItem]]:
        return self.sequencer.current_harmony_item, self.sequencer.current_chord_item

    def stop(self):
        logger.info("stopped")

        self.state = SequencerState.stopped

        self.sequencer.reset()

        self.midi_manager.terminate_output_thread()

    def finished(self):
        logger.info("finished")

        self.state = SequencerState.stopped
        self.sequencer.reset()

        self.grid_ended.emit()
