import logging

from PySide6.QtCore import QObject, Signal

from beethoven.adapters.factory import Adapters
from beethoven.settings import AppSettings, save_settings, serialize_settings
from beethoven.ui.managers.midi import MidiManager
from beethoven.ui.managers.sequencer import SequencerManager

logger = logging.getLogger("manager.app")


class AppManager(QObject):
    configuration_changed = Signal()

    def __init__(self, *args, settings: AppSettings, adapters: Adapters, **kwargs):
        super(AppManager, self).__init__(*args, **kwargs)
        self.settings = settings
        self.adapters = adapters

        self.midi = MidiManager(settings=self.settings, midi_adapter=self.adapters.midi)
        self.sequencer = SequencerManager(
            settings=self.settings, adapters=self.adapters, midi_manager=self.midi
        )

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
