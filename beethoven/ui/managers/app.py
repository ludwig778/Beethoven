import logging
from logging import getLogger
from typing import Callable, Optional

from hartware_lib.adapters.file import FileAdapter
from PySide6.QtCore import QObject, Signal

from beethoven.adapters.factory import Adapters
from beethoven.models import Grid
from beethoven.settings import AppSettings, save_settings, serialize_settings
from beethoven.ui.managers.midi import MidiManager
from beethoven.ui.threads import MidiOutputThread
from beethoven.ui.utils import setup_players

logger = getLogger("manager.app")


class AppManager(QObject):
    grid_ended = Signal()
    configuration_changed = Signal()

    def __init__(self, *args, settings: AppSettings, adapters: Adapters, **kwargs):
        super(AppManager, self).__init__(*args, **kwargs)
        self.settings = settings
        self.adapters = adapters

        self.setting_file = FileAdapter(file_path=settings.config_file.path)
        self.midi = MidiManager(settings=self.settings, midi_adapter=self.adapters.midi)

        self.configuration_changed.connect(self.on_configuration_change)

    def on_configuration_change(self, *args, **kwargs):
        logger.info("configuration changed")

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(serialize_settings(self.settings))

        save_settings(self.settings)

    def close(self):
        logger.debug("shutting down...")

        self.midi.terminate_threads()

        self.adapters.midi.shutdown()
        self.adapters.midi.close_all_outputs()
        self.adapters.midi.close_input(self.midi_input_handler.current_input)

    def play_grid(
        self,
        grid: Grid,
        preview: bool = False,
        on_grid_part_change: Optional[Callable] = None,
        on_grid_part_end: Optional[Callable] = None,
    ):
        self.midi.terminate_output_thread()

        if preview:
            player_settings = [self.settings.player.preview]
        else:
            player_settings = self.settings.player.players

        players = setup_players(
            midi_adapter=self.adapters.midi, player_settings=player_settings
        )

        self.midi.output_thread = MidiOutputThread(
            midi_adapter=self.adapters.midi,
            grid=grid,
            players=players,
            on_grid_part_change=on_grid_part_change,
            on_grid_part_end=self.grid_ended.emit,
        )
        self.midi.output_thread.start()
