from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow

from beethoven.ui.apps.compose import ComposeWidget
from beethoven.ui.apps.harmony_trainer import HarmonyTrainerWidget
from beethoven.ui.components.combobox.widget_selector import WidgetSelectorComboBox
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
        )
        self.stack.setup()
        self.stack.setContentsMargins(6, 6, 6, 6)

        self.setCentralWidget(self.stack)

    def set_menubar(self):
        menubar = self.menuBar()

        file = menubar.addMenu("File")

        quit = QAction("Quit", self)
        quit.setShortcut("Q")
        quit.triggered.connect(self.close)

        file.addAction(quit)

    def run_dialog(self, dialog_class, **kwargs):
        def setup_dialog():
            dialog = dialog_class(**kwargs)
            dialog.exec()

        return setup_dialog
