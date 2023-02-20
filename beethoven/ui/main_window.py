from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow

from beethoven.ui.apps.compose import ComposeWidget
from beethoven.ui.apps.harmony_trainer import HarmonyTrainerWidget
from beethoven.ui.components.combobox.widget_selector import WidgetSelectorComboBox
from beethoven.ui.dialogs.midi import MidiDialog
from beethoven.ui.dialogs.player import PlayerDialog
from beethoven.ui.dialogs.tuning import TuningDialog
from beethoven.ui.managers import AppManager


class MainWindow(QMainWindow):
    def __init__(self, *args, manager: AppManager, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Beethoven")

        self.manager = manager

        self.set_menubar()

        self.stack = WidgetSelectorComboBox(
            widgets={
                "Compose": ComposeWidget(manager=manager),
                "Harmony Trainer": HarmonyTrainerWidget(manager=manager),
                # "Piano": PianoTrainerWidget(manager=manager),
            },
            parent=self,
        )
        self.stack.setup()
        self.stack.setContentsMargins(6, 6, 6, 6)

        self.setCentralWidget(self.stack)

    def set_menubar(self):
        menubar = self.menuBar()

        file = menubar.addMenu("File")
        settings = menubar.addMenu("Settings")

        tuning_settings = QAction("Tunings", self)
        tuning_settings.triggered.connect(
            self.run_dialog(TuningDialog, manager=self.manager)
        )

        midi_settings = QAction("Midi", self)
        midi_settings.triggered.connect(
            self.run_dialog(MidiDialog, manager=self.manager)
        )

        player_settings = QAction("Players", self)
        player_settings.triggered.connect(
            self.run_dialog(PlayerDialog, manager=self.manager)
        )

        quit = QAction("Quit", self)
        quit.setShortcut("Q")
        quit.triggered.connect(self.close)

        file.addAction(quit)

        settings.addActions(
            [
                tuning_settings,
                midi_settings,
                player_settings,
            ]
        )

    def run_dialog(self, dialog_class, **kwargs):
        def setup_dialog():
            dialog = dialog_class(**kwargs)
            dialog.exec()

        return setup_dialog
