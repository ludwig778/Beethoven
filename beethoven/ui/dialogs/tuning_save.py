import logging
from typing import Tuple

from PySide6.QtWidgets import QDialog, QLabel, QLineEdit

from beethoven.settings import TuningSettings
from beethoven.ui.components.buttons import Button
from beethoven.ui.layouts import (Spacing, Stretch, horizontal_layout,
                                  vertical_layout)

logger = logging.getLogger("dialog.tuning_save")


class TuningSaveDialog(QDialog):
    def __init__(self, *args, tuning_settings: TuningSettings, **kwargs):
        super(TuningSaveDialog, self).__init__(*args, **kwargs)

        self.tuning_settings = tuning_settings

        self.text_label = QLabel("Choose the tuning name: ")
        self.input_box = QLineEdit()

        self.duplicate_error_label = QLabel()
        self.duplicate_error_label.setObjectName("error_label")

        self.ok_button = Button("Ok", object_name="green")
        self.cancel_button = Button("Cancel", object_name="red")

        self.ok_button.setEnabled(False)
        self.input_box.setMaxLength(20)

        self.input_box.textChanged.connect(self.update)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self.setLayout(
            vertical_layout(
                [
                    self.text_label,
                    Spacing(size=10),
                    self.input_box,
                    Spacing(size=2),
                    horizontal_layout(
                        [
                            Stretch(),
                            self.duplicate_error_label,
                            Stretch(),
                        ]
                    ),
                    Stretch(),
                    horizontal_layout(
                        [
                            self.ok_button,
                            self.cancel_button,
                        ]
                    ),
                ],
                margins=(10, 10, 10, 10),
            )
        )

    def update(self, tuning_name):
        existing_tuning_names = self.tuning_settings.defaults.keys()

        if tuning_name in existing_tuning_names:
            self.ok_button.setEnabled(False)
            self.duplicate_error_label.setText("Name already taken")
        else:
            self.ok_button.setEnabled(tuning_name != "")
            self.duplicate_error_label.setText("")

    def getText(self) -> Tuple[bool, str]:
        return bool(self.exec()), self.input_box.text()
