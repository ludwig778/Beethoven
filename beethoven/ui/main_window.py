from PySide6.QtWidgets import QMainWindow

from beethoven.ui.apps.chord_trainer import ChordTrainerWidget
from beethoven.ui.apps.compose import ComposeWidget
from beethoven.ui.components.widget_selector import ComboBoxSelectedWidget
from beethoven.ui.managers import AppManager


class MainWindow(QMainWindow):
    def __init__(self, *args, manager: AppManager, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.manager = manager

        self.setWindowTitle("Beethoven")
        self.setFixedSize(500, 500)

        self.setCentralWidget(
            ComboBoxSelectedWidget(
                manager=manager,
                widgets={
                    "Chord Trainer": ChordTrainerWidget(manager=manager),
                    "Composer": ComposeWidget(manager=manager),
                },
            )
        )
