import logging
from typing import Tuple

from PySide6.QtWidgets import QDialog, QLabel, QLineEdit

from beethoven.ui.components.buttons import Button
from beethoven.ui.layouts import Spacing, horizontal_layout, vertical_layout
from beethoven.ui.managers.app import AppManager

logger = logging.getLogger("dialog.midi_add")


class MidiAddDialog(QDialog):
    def __init__(self, *args, manager: AppManager, **kwargs):
        super(MidiAddDialog, self).__init__(*args, **kwargs)

        self.manager = manager

        self.text_label = QLabel("Choose Midi output name :")
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
                    Spacing(size=10),
                    self.input_box,
                    Spacing(size=10),
                    horizontal_layout([self.ok_button, self.cancel_button]),
                ],
                margins=(10, 10, 10, 10),
            )
        )

    def on_text_change(self, output_name):
        self.ok_button.setEnabled(
            bool(
                output_name
                and output_name
                not in [
                    *self.manager.settings.midi.opened_outputs,
                    *self.manager.adapters.midi.outputs.keys(),
                ]
            )
        )

    def getText(self) -> Tuple[bool, str]:
        return bool(self.exec()), self.input_box.text()
