import atexit
from logging import getLogger
from pathlib import Path

from PySide6.QtWidgets import QApplication

from beethoven.ui.apps.main_window import MainWindow
from beethoven.ui.managers import AppManager
from beethoven.ui.stylesheet import get_stylesheet

logger = getLogger("ui.main")


def main():
    app = QApplication([])
    app.setStyleSheet(get_stylesheet())

    setting_path = Path(".", "config.ui.json")
    manager = AppManager(setting_path=setting_path)

    atexit.register(manager.midi.terminate_threads)

    window = MainWindow(manager=manager)
    window.setWindowTitle("Beethoven")

    # set_size_policies([w], QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
