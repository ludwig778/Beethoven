import atexit
import logging

from PySide6.QtWidgets import QMainWindow

from beethoven.adapters.factory import get_adapters
from beethoven.settings import AppSettings
from beethoven.ui.main_window import MainWindow
from beethoven.ui.managers import AppManager

logger = logging.getLogger("ui.main")


def setup_main_window() -> QMainWindow:
    manager = AppManager(settings=AppSettings.load(), adapters=get_adapters())
    print("OUT" * 33)
    print(manager)

    atexit.register(manager.midi.terminate_threads)

    return MainWindow(manager=manager)
