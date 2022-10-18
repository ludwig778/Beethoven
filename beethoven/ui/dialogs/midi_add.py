from logging import getLogger
from typing import List, Tuple

from PySide6.QtWidgets import QDialog, QLabel, QLineEdit

from beethoven.ui.components.buttons import Button
from beethoven.ui.layouts import horizontal_layout, vertical_layout

logger = getLogger("dialog.midi_add")


class MidiAddDialog(QDialog):
    def __init__(self, *args, existing_output_names: List[str], **kwargs):
        super(MidiAddDialog, self).__init__(*args, **kwargs)

        self.existing_output_names = existing_output_names

        self.text_label = QLabel("Choose Midi output name:")
        self.input_box = QLineEdit()

        self.ok_button = Button("Ok")
        self.cancel_button = Button("Cancel")

        self.ok_button.setEnabled(False)

        self.input_box.textChanged.connect(self.on_text_change)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self.setLayout(
            vertical_layout(
                [
                    self.text_label,
                    self.input_box,
                    horizontal_layout([self.ok_button, self.cancel_button]),
                ]
            )
        )

    def on_text_change(self, output_name):
        self.ok_button.setEnabled(
            bool(output_name and output_name not in self.existing_output_names)
        )

    def getText(self) -> Tuple[bool, str]:
        return bool(self.exec()), self.input_box.text()
