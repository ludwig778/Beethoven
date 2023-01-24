from functools import partial

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow

from beethoven.ui.apps.compose import ComposeWidget
from beethoven.ui.apps.harmony_trainer import HarmonyTrainerWidget
from beethoven.ui.apps.piano_trainer import PianoTrainerWidget
from beethoven.ui.components.combobox.widget_selector import WidgetSelectorComboBox
from beethoven.ui.components.widget_stack import StackedWidget
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

        self.stack = StackedWidget(
            widgets={
                "Compose": ComposeWidget(manager=manager),
                "Trainer": WidgetSelectorComboBox(
                    widgets={
                        "Harmony": HarmonyTrainerWidget(manager=manager),
                        "Piano": PianoTrainerWidget(manager=manager),
                    },
                    parent=self
                )
            },
            parent=self
        )
        self.stack.setContentsMargins(6, 6, 6, 6)

        self.setCentralWidget(self.stack)

    def set_menubar(self):
        menubar = self.menuBar()

        file = menubar.addMenu("File")
        mode = menubar.addMenu("Mode")
        settings = menubar.addMenu("Settings")

        compose_mode = QAction("Compose Mode", self)
        compose_mode.triggered.connect(partial(self.set_stack_widget_index, 0))

        trainer_mode = QAction("Trainer Mode", self)
        trainer_mode.triggered.connect(partial(self.set_stack_widget_index, 1))

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

        mode.addActions(
            [
                compose_mode,
                trainer_mode,
            ]
        )

        settings.addActions(
            [
                tuning_settings,
                midi_settings,
                player_settings,
            ]
        )

        self.mode_menu = mode

    def set_stack_widget_index(self, stack_index):
        self.stack.set_index(stack_index)

    def run_dialog(self, dialog_class, **kwargs):
        def setup_dialog():
            dialog = dialog_class(**kwargs)
            dialog.exec()

        return setup_dialog
