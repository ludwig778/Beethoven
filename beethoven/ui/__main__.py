import atexit
from logging import getLogger
from pathlib import Path

from PySide6.QtWidgets import QApplication

from beethoven.ui.main_window import MainWindow
from beethoven.ui.managers import AppManager
from beethoven.ui.stylesheet import get_stylesheet

logger = getLogger("ui.main")


def main():
    manager = AppManager(setting_path=Path(".", "config.ui.json"))

    atexit.register(manager.midi.terminate_threads)

    window = MainWindow(manager=manager)
    window.setWindowTitle("Beethoven")

    # set_size_policies([w], QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
    window.show()


if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(get_stylesheet())

    main()

    app.exec()
