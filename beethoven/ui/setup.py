import atexit
from logging import getLogger

from PySide6.QtWidgets import QMainWindow

from beethoven.adapters.factory import get_adapters
from beethoven.settings import setup_settings
from beethoven.ui.main_window import MainWindow
from beethoven.ui.managers import AppManager

logger = getLogger("ui.main")


def setup_main_window() -> QMainWindow:
    manager = AppManager(settings=setup_settings(), adapters=get_adapters())

    atexit.register(manager.midi.terminate_threads)

    main_window = MainWindow(manager=manager)
    # from beethoven.ui.dialogs.tuning import TuningDialog
    # main_window = TuningDialog(manager=manager)
    # from beethoven.ui.dialogs.midi import MidiDialog
    # main_window = MidiDialog(manager=manager)
    # from beethoven.ui.dialogs.player import PlayerDialog
    # main_window = PlayerDialog(manager=manager)
    # from beethoven.ui.dialogs.midi_add import MidiAddDialog
    # main_window = MidiAddDialog(manager=manager)
    # from beethoven.ui.dialogs.tuning_save import TuningSaveDialog
    # main_window = TuningSaveDialog(tuning_settings=manager.settings.tuning)

    return main_window
