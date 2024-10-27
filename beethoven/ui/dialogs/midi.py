import logging

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QLabel

from beethoven.ui.components.buttons import Button
from beethoven.ui.components.combobox.midi_input import MidiInputComboBox
from beethoven.ui.components.selectors import MidiOutputSelector
from beethoven.ui.constants import DEFAULT_MIDI_INPUT
from beethoven.ui.dialogs.midi_add import MidiAddDialog
from beethoven.ui.layouts import Spacing, horizontal_layout, vertical_layout
from beethoven.ui.managers import AppManager

logger = logging.getLogger("dialog.midi")


class MidiDialog(QDialog):
    configuration_changed = Signal()

    def __init__(self, *args, manager: AppManager, **kwargs):
        super(MidiDialog, self).__init__(*args, **kwargs)

        self.manager = manager

        self.input_combobox = MidiInputComboBox(manager=manager)
        self.output_selector = MidiOutputSelector(manager=manager)

        self.input_refresh_button = Button("Refresh")
        self.input_refresh_button.setObjectName("refresh")

        self.ok_button = Button("OK", object_name="blue")
        self.add_output_button = Button("Add", object_name="green")
        self.delete_output_button = Button("Delete", object_name="red")

        self.input_combobox.value_changed.connect(self.handle_midi_input_change)
        self.input_refresh_button.clicked.connect(self.input_combobox.refresh)

        self.ok_button.clicked.connect(self.close)
        self.add_output_button.clicked.connect(self.add_output)
        self.delete_output_button.clicked.connect(self.output_selector.delete_selected_outputs)

        self.setLayout(
            vertical_layout(
                [
                    QLabel("Midi Input"),
                    Spacing(size=8),
                    self.input_combobox,
                    Spacing(size=10),
                    self.input_refresh_button,
                    Spacing(size=18),
                    QLabel("Midi Outputs"),
                    Spacing(size=8),
                    self.output_selector,
                    Spacing(size=10),
                    horizontal_layout(
                        [
                            self.ok_button,
                            self.add_output_button,
                            self.delete_output_button,
                        ]
                    ),
                ],
                margins=(10, 10, 10, 10),
            )
        )

    def add_output(self):
        logger.debug("adding output...")

        dialog = MidiAddDialog(manager=self.manager)

        ok, output_name = dialog.getText()

        if not ok:
            logger.info("adding output aborted")

            return

        logger.info(f"adding output: {output_name}")

        self.output_selector.add(output_name)

    def handle_midi_input_change(self, name):
        logger.info(f"set input to {name or 'none'}")

        if name != DEFAULT_MIDI_INPUT:
            self.manager.settings.midi.selected_input = name
        else:
            self.manager.settings.midi.selected_input = None

        self.manager.midi.update_input(name)

        self.manager.configuration_changed.emit()
