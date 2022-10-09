import json
from logging import getLogger
import logging
from pathlib import Path

from hartware_lib.adapters.file import FileAdapter
from PySide6.QtCore import QObject, Signal

from beethoven.adapters.factory import get_adapters
from beethoven.models import Grid
from beethoven.ui.managers.midi import MidiManager
from beethoven.ui.settings import AppSettings, get_default_settings
from beethoven.ui.threads import MidiOutputThread
from beethoven.ui.utils import setup_players

logger = getLogger("manager.app")


class AppManager(QObject):
    configuration_changed = Signal()

    def __init__(self, *args, setting_path: Path, **kwargs):
        # adapters: Adapters, settings: AppSettings, **kwargs):
        super(AppManager, self).__init__(*args, **kwargs)

        self.setting_file = FileAdapter(file_path=setting_path)

        if self.setting_file.exists():
            self.settings = AppSettings(**self.setting_file.read_json())
        else:
            if not self.setting_file.file_path.parent.exists():
                self.setting_file.create_parent_dir()

            self.settings = get_default_settings()
            self.setting_file.save_json(self.settings.dict())

        self.adapters = get_adapters()

        self.midi = MidiManager(settings=self.settings, midi_adapter=self.adapters.midi)

        self.configuration_changed.connect(self.on_configuration_change)

        """
        self.midi_input_handler = MidiInputHandler(midi_adapter=self.adapters.midi)
        self.midi_input_handler.set_input(self.settings.midi.selected_input)

        self.midi_output_handler = MidiOutputHandler(
            settings=self.settings,
            midi_adapter=self.adapters.midi
        )
        """

    def on_configuration_change(self, *args, **kwargs):
        logger.info("configuration changed")

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(json.dumps(self.settings.dict(), indent=2))

        self.setting_file.save_json(self.settings.dict())

    def close(self):
        logger.debug("shutting down...")

        self.midi.terminate_threads()

        self.adapters.midi.shutdown()
        self.adapters.midi.close_all_outputs()
        self.adapters.midi.close_input(self.midi_input_handler.current_input)

    def play_grid(self, grid: Grid, preview: bool = False):
        self.midi.terminate_output_thread()

        if preview:
            player_settings = [self.settings.player.preview]
        else:
            player_settings = self.settings.player.players

        players = setup_players(
            midi_adapter=self.adapters.midi, player_settings=player_settings
        )

        self.midi.output_thread = MidiOutputThread(
            midi_adapter=self.adapters.midi, grid=grid, players=players
        )
        self.midi.output_thread.start()
