import logging
from typing import Tuple

from PySide6.QtWidgets import QDialog, QLabel, QLineEdit

from beethoven.ui.components.buttons import Button
from beethoven.ui.layouts import (Spacing, Stretch, horizontal_layout,
                                  vertical_layout)
from beethoven.ui.managers.app import AppManager

logger = logging.getLogger("dialog.midi_add")


class MidiAddDialog(QDialog):
    def __init__(self, *args, manager: AppManager, **kwargs):
        super(MidiAddDialog, self).__init__(*args, **kwargs)

        self.manager = manager

        self.text_label = QLabel("Choose Midi output name :")
        self.input_box = QLineEdit()

        self.duplicate_error_label = QLabel()
        self.duplicate_error_label.setObjectName("error_label")

        self.ok_button = Button("Ok", object_name="green")
        self.cancel_button = Button("Cancel", object_name="red")

        self.ok_button.setEnabled(False)

        self.input_box.textChanged.connect(self.on_text_change)
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
                    horizontal_layout([self.ok_button, self.cancel_button]),
                ],
                margins=(10, 10, 10, 10),
            )
        )

    def on_text_change(self, output_name: str):
        if output_name == "":
            self.ok_button.setEnabled(False)
            self.duplicate_error_label.setText("")
        elif (
            output_name in self.manager.settings.midi.opened_outputs
            or output_name in self.manager.adapters.midi.outputs.keys()
        ):
            self.ok_button.setEnabled(False)
            self.duplicate_error_label.setText("Output already exists")
        else:
            self.ok_button.setEnabled(True)
            self.duplicate_error_label.setText("")

    def getText(self) -> Tuple[bool, str]:
        return bool(self.exec()), self.input_box.text()
