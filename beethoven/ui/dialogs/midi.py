from logging import getLogger

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QDialog

from beethoven.ui.components.buttons import Button
from beethoven.ui.components.combobox.midi_input import MidiInputComboBox
from beethoven.ui.components.selectors import MidiOutputSelector
from beethoven.ui.constants import DEFAULT_MIDI_INPUT
from beethoven.ui.dialogs.midi_add import MidiAddDialog
from beethoven.ui.layouts import horizontal_layout, vertical_layout
from beethoven.ui.managers import AppManager
from beethoven.ui.utils import block_signal

logger = getLogger("dialog.midi")


class MidiDialog(QDialog):
    configuration_changed = Signal()

    def __init__(self, *args, manager: AppManager, **kwargs):
        super(MidiDialog, self).__init__(*args, **kwargs)

        self.manager = manager

        self.input_combobox = MidiInputComboBox(
            manager=manager, value=self.manager.settings.midi.selected_input
        )
        # self.setup_inputs()

        self.input_refresh_button = Button("Refresh")
        self.output_selector = MidiOutputSelector()
        self.ok_button = Button("OK")
        self.add_output_button = Button("Add")
        self.delete_output_button = Button("Delete")
        self.setup_outputs()

        self.input_combobox.currentTextChanged.connect(self.update_input)
        self.input_refresh_button.clicked.connect(self.input_combobox.setup_items)
        self.ok_button.clicked.connect(self.close)
        self.add_output_button.clicked.connect(self.add_output)
        self.delete_output_button.clicked.connect(self.delete_output)

        self.setLayout(
            vertical_layout(
                [
                    QLabel("Midi Input"),
                    horizontal_layout(
                        [
                            self.input_combobox,
                            self.input_refresh_button,
                        ]
                    ),
                    QLabel("Midi Outputs"),
                    self.output_selector,
                    horizontal_layout(
                        [
                            self.ok_button,
                            self.add_output_button,
                            self.delete_output_button,
                        ]
                    ),
                ]
            )
        )

    def setup_inputs(self):
        logger.info("refreshing inputs")

        with block_signal([self.input_combobox]):
            self.input_combobox.clear()

            self.input_combobox.addItem(DEFAULT_MIDI_INPUT)

            items = sorted(set(self.manager.adapters.midi.available_inputs))
            self.input_combobox.addItems(items)

            if self.manager.settings.midi.selected_input in items:
                self.input_combobox.setCurrentText(
                    self.manager.settings.midi.selected_input
                )

    def setup_outputs(self):
        for output_name in self.manager.settings.midi.opened_outputs:
            self.output_selector.add_output(output_name)

    def update_input(self, input_name):
        logger.info(f"set input to {input_name or 'none'}")

        if input_name != DEFAULT_MIDI_INPUT:
            self.manager.settings.midi.selected_input = input_name
        else:
            self.manager.settings.midi.selected_input = None

        self.manager.configuration_changed.emit()

    def add_output(self):
        logger.debug("adding output...")

        dialog = MidiAddDialog(
            existing_output_names=[
                *self.manager.settings.midi.opened_outputs,
                *self.manager.adapters.midi.outputs.keys(),
            ]
        )

        ok, output_name = dialog.getText()

        if not ok:
            logger.info("adding output aborted")

            return

        logger.info(f"adding output: {output_name}")

        self.manager.adapters.midi.open_output(output_name)

        self.output_selector.add_output(output_name)

        self.manager.settings.midi.opened_outputs.append(output_name)
        self.manager.configuration_changed.emit()

    def delete_output(self):
        output_names = self.output_selector.current_output_names

        logger.info(f"deleting outputs: {', '.join(output_names) or 'none selected'}")

        if not output_names:
            return

        for output_name in output_names:
            self.manager.adapters.midi.close_output(output_name)
            self.manager.settings.midi.opened_outputs.remove(output_name)

            self.output_selector.delete_output(output_name)

        self.manager.configuration_changed.emit()
