from PySide6.QtWidgets import QApplication
from beethoven.ui.__main__ import main as run_main_window

from beethoven.ui.stylesheet import get_stylesheet


def test_main_ui():
    print("\n\n")

    qt_application = QApplication([])
    qt_application.setStyleSheet(get_stylesheet())

    run_main_window()

    qt_application.exec()

    print("\n\n")
