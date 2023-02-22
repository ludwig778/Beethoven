from logging import getLogger
import traceback

from PySide6.QtWidgets import QApplication

from beethoven.ui.setup import setup_main_window
from beethoven.ui.stylesheet import get_stylesheet

logger = getLogger("ui.main")


def run():
    try:
        app = QApplication([])
        app.setStyleSheet(get_stylesheet())

        main_window = setup_main_window()
        main_window.show()

        app.exec()
    except Exception:
        logger.critical(traceback.format_exc())


if __name__ == "__main__":
    run()
