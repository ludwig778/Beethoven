import atexit
import logging

from PySide6.QtWidgets import QMainWindow

from beethoven.adapters.factory import get_adapters
from beethoven.settings import setup_settings
from beethoven.ui.main_window import MainWindow
from beethoven.ui.managers import AppManager

logger = logging.getLogger("ui.main")


def setup_main_window() -> QMainWindow:
    manager = AppManager(settings=setup_settings(), adapters=get_adapters())

    atexit.register(manager.midi.terminate_threads)

    return MainWindow(manager=manager)
