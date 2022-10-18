from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QAction

from beethoven.ui.apps.chord_trainer import ChordTrainerWidget
from beethoven.ui.apps.compose import ComposeWidget
from beethoven.ui.components.widget_selector import ComboBoxSelectedWidget
from beethoven.ui.dialogs.midi import MidiDialog
from beethoven.ui.dialogs.player import PlayerDialog
from beethoven.ui.dialogs.tuning import TuningDialog
from beethoven.ui.managers import AppManager


class MainWindow(QMainWindow):
    def __init__(self, *args, manager: AppManager, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.manager = manager

        self.set_menubar()
        self.setWindowTitle("Beethoven")
        self.setFixedSize(500, 500)

        self.setCentralWidget(
            ComboBoxSelectedWidget(
                manager=manager,
                widgets={
                    "Composer": ComposeWidget(manager=manager),
                    "Chord Trainer": ChordTrainerWidget(manager=manager),
                },
            )
        )

    def set_menubar(self):
        menubar = self.menuBar()

        file = menubar.addMenu("File")
        settings = menubar.addMenu("Settings")

        tuning_settings = QAction("Tunings", self)
        tuning_settings.triggered.connect(self.run_dialog(TuningDialog, manager=self.manager))

        midi_settings = QAction("Midi", self)
        midi_settings.triggered.connect(self.run_dialog(MidiDialog, manager=self.manager))

        player_settings = QAction("Players", self)
        player_settings.triggered.connect(self.run_dialog(PlayerDialog, manager=self.manager))

        quit = QAction("Quit", self)
        quit.setShortcut("Q")
        quit.triggered.connect(self.close)

        file.addAction(quit)

        settings.addActions([
            tuning_settings,
            midi_settings,
            player_settings,
        ])

    def run_dialog(self, dialog_class, **kwargs):
        def setup_dialog():
            dialog = dialog_class(**kwargs)
            dialog.exec()

        return setup_dialog
