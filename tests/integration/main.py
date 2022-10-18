from PySide6.QtWidgets import QApplication
from beethoven.ui.setup import setup_main_window

from beethoven.ui.stylesheet import get_stylesheet


def test_main_ui():
    print("\n\n")

    qt_application = QApplication([])
    qt_application.setStyleSheet(get_stylesheet())

    main_window = setup_main_window()
    main_window.show()

    qt_application.exec()

    print("\n\n")
