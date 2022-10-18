from pathlib import Path
from typing import Dict

from PySide6.QtWidgets import QComboBox, QWidget, QApplication

from beethoven.ui.apps.chord_trainer import ChordTrainerWidget
from beethoven.ui.apps.compose import ComposeWidget
from beethoven.ui.components.widget_selector import ComboBoxSelectedWidget
from beethoven.ui.layouts import stacked_layout, vertical_layout
from beethoven.ui.managers.app import AppManager
from beethoven.ui.stylesheet import get_stylesheet


def test_live_ui():
    print("\n\n")

    qt_application = QApplication([])
    qt_application.setStyleSheet(get_stylesheet())

    manager = AppManager(setting_path=Path(".", "config.ui.json"))

    widgets = {
        "Chord Trainer": ChordTrainerWidget(manager=manager),
        "Composer": ComposeWidget(manager=manager),
    }

    widget = ComboBoxSelectedWidget(manager=manager, widgets=widgets)
    widget.setWindowTitle("Beethoven")
    widget.show()

    qt_application.exec()

    print("\n\n")
