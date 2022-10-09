from logging import getLogger
from typing import Tuple

from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from beethoven.ui.settings import TuningSettings

logger = getLogger("dialog.tuning_save")


class TuningSaveDialog(QDialog):
    def __init__(self, *args, tuning_settings: TuningSettings, **kwargs):
        super(TuningSaveDialog, self).__init__(*args, **kwargs)

        self.tuning_settings = tuning_settings

        self.setup()

    def setup(self):
        logger.debug("setup")

        self.text_label = QLabel("Choose the tuning name:")
        self.input_box = QLineEdit()

        self.duplicate_error_label = QLabel(
            "Choose another name, this one's already taken"
        )

        self.ok_button = QPushButton("Ok")
        self.cancel_button = QPushButton("Cancel")

        self.duplicate_error_label.setVisible(False)
        self.ok_button.setEnabled(False)

        self.input_box.textChanged.connect(self.update)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self.setLayout(self.get_layout())

    def update(self, tuning_name):
        existing_tuning_names = self.tuning_settings.defaults.keys()

        if tuning_name in existing_tuning_names:
            self.ok_button.setEnabled(False)
            self.duplicate_error_label.setVisible(True)
        else:
            self.ok_button.setEnabled(tuning_name != "")
            self.duplicate_error_label.setVisible(False)

    def getText(self) -> Tuple[bool, str]:
        return bool(self.exec()), self.input_box.text()

    def get_layout(self):
        main_layout = QVBoxLayout()

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.ok_button)
        buttons_layout.addWidget(self.cancel_button)

        main_layout.addWidget(self.text_label)
        main_layout.addWidget(self.input_box)
        main_layout.addWidget(self.duplicate_error_label)
        main_layout.addLayout(buttons_layout)

        return main_layout
