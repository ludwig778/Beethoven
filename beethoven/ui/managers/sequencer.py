import logging
from enum import Enum, auto

from PySide6.QtCore import QObject, QThread, Signal

from beethoven.adapters.factory import Adapters
from beethoven.models import ChordItem, HarmonyItem
from beethoven.sequencer.objects import HarmonyItemSelector, SystemPlayer
from beethoven.sequencer.runner import Sequencer
from beethoven.sequencer.utils import setup_players
from beethoven.settings import AppSettings, PlayerSetting
from beethoven.ui.managers.midi import MidiManager
from beethoven.ui.threads import MidiOutputThread

logger = logging.getLogger("manager.sequencer")


class SequencerState(Enum):
    playing = auto()
    playing_preview = auto()
    stopped = auto()


class SequencerManager(QObject):
    grid_play = Signal(object)
    grid_stop = Signal()
    grid_ended = Signal()

    items_change = Signal(HarmonyItem, ChordItem)

    def __init__(
        self, *args, settings: AppSettings, adapters: Adapters, midi_manager: MidiManager, **kwargs
    ):
        super(SequencerManager, self).__init__(*args, **kwargs)

        self.settings = settings
        self.adapters = adapters
        self.midi_manager = midi_manager
        self.harmony_iterator = HarmonyItemSelector([])

        self.state = SequencerState.stopped

        self._system_player = SystemPlayer(PlayerSetting())

        self.grid_play.connect(self._play)
        self.grid_stop.connect(self._stop)

    def set_harmony_iterator(self, harmony_iterator: HarmonyItemSelector):
        self.harmony_iterator = harmony_iterator

    # def get_players(self):
    #     return [*self.players, self._system_player]

    def get_metronome_player(self):
        return setup_players(
            midi_adapter=self.adapters.midi,
            player_settings=[self.settings.player.metronome]
        )

    def get_players(self, preview: bool = False):
        if preview:
            player_settings = [self.settings.player.preview]
        else:
            player_settings = self.settings.player.players

        players = setup_players(
            midi_adapter=self.adapters.midi,
            player_settings=player_settings
        )
        # players.append(self._system_player)

        return players

    def is_playing(self) -> bool:
        return self.state in (SequencerState.playing, SequencerState.playing_preview)

    def is_playing_preview(self) -> bool:
        return self.state == SequencerState.playing_preview

    def is_stopped(self) -> bool:
        return self.state == SequencerState.stopped

    def play(self, **kwargs):
        self.grid_play.emit(kwargs)

    def _play(self, params):
        if params.get("if_playing") and not self.is_playing():
            print("Sequencer::Play : not playing, skipping...")
            return
        preview = params.get("preview", False)
        # continuous = params.get("continuous", False)

        # params.get("preview", not self.is_playing() or self.is_playing_preview())  # params.get("preview", False)
        print(f"SequencerManager :: Play  : {self.state = }  -  {preview = }        ({params = })")
        logger.info("playing")

        if not self.is_stopped():
            self.midi_manager.terminate_output_thread()

        self.state = SequencerState.playing_preview if preview else SequencerState.playing

        sequencer = Sequencer(
            midi_adapter=self.adapters.midi,
            players=self.get_players(preview=preview),
            harmony_iterator=self.harmony_iterator,
            preview=preview,
            items_change=self.items_change
        )
        self.midi_manager.output_thread = MidiOutputThread(
            midi_adapter=self.adapters.midi,
            sequencer=sequencer
        )
        self.midi_manager.output_thread.start()
        self.midi_manager.output_thread.setPriority(QThread.TimeCriticalPriority)
        self.midi_manager.output_thread.finished.connect(self.finished)
        # self.midi_manager.output_thread.timeout.connect(self.finished)

    def stop(self, **kwargs):
        print(" ==== STOP")
        self.grid_stop.emit()

    def _stop(self):
        print("SequencerManager::Stop")
        logger.info("stopped")
        if not self.is_stopped():
            self.midi_manager.terminate_output_thread()
            # print("OUT 1")
            # self.midi_manager.output_thread.timeout.disconnect()
            # self.midi_manager.output_thread.stop()
            # self.midi_manager.output_thread = None
            # print("OUT 2")
        self.state = SequencerState.stopped
        # self.sequencer.reset()
        # self.midi_manager.terminate_output_thread()

    def finished(self):
        print("SequencerManager::Finished")
        logger.info("finished")

        if not self.is_stopped():
            self.midi_manager.terminate_output_thread()
            # print("OUT 1")
            # self.midi_manager.output_thread.timeout.disconnect()
            # self.midi_manager.output_thread.stop()
            # self.midi_manager.output_thread = None
            # print("OUT 2")
        self.state = SequencerState.stopped
        # self.sequencer.reset()
        self.grid_ended.emit()
        return
