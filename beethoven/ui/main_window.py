from PySide6.QtWidgets import QMainWindow, QPushButton

from beethoven.ui.apps.chord_trainer import ChordTrainerWidget
from beethoven.ui.apps.compose import ComposeWidget
from beethoven.ui.layouts import horizontal_layout, stacked_layout, vertical_layout
from beethoven.ui.managers import AppManager


class MainWindow(QMainWindow):
    def __init__(self, *args, manager: AppManager, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.manager = manager

        self.ok_button = QPushButton("Ok")
        self.training_button = QPushButton("Training")
        self.compose_button = QPushButton("Compose")

        self.stacked_layout = stacked_layout(
            [
                ChordTrainerWidget(manager=self.manager),
                ComposeWidget(manager=self.manager),
            ]
        )

        for button in [self.ok_button, self.training_button, self.compose_button]:
            button.setStyleSheet("height:33px;")

        self.ok_button.clicked.connect(self.close)
        self.training_button.clicked.connect(lambda: self.set_widget(0))
        self.compose_button.clicked.connect(lambda: self.set_widget(1))

        self.setCentralWidget(
            vertical_layout(
                [
                    self.stacked_layout,
                    horizontal_layout(
                        [
                            self.ok_button,
                            self.training_button,
                            self.compose_button,
                        ]
                    ),
                ],
                object_name="main_window",
            )
        )

        self.setFixedSize(500, 500)

    def set_widget(self, index):
        self.stacked_layout.setCurrentIndex(int(index))
