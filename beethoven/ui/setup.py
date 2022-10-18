import atexit
from logging import getLogger
from pathlib import Path

from PySide6.QtWidgets import QMainWindow

from beethoven.ui.main_window import MainWindow
from beethoven.ui.managers import AppManager

logger = getLogger("ui.main")


def setup_main_window() -> QMainWindow:
    manager = AppManager(setting_path=Path(".", "config.ui.json"))

    atexit.register(manager.midi.terminate_threads)

    main_window = MainWindow(manager=manager)

    return main_window
