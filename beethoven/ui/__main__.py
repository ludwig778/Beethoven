from logging import getLogger

from PySide6.QtWidgets import QApplication
from beethoven.ui.setup import setup_main_window

from beethoven.ui.stylesheet import get_stylesheet

logger = getLogger("ui.main")


if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(get_stylesheet())

    main_window = setup_main_window()
    main_window.show()

    app.exec()
