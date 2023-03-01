from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox

from beethoven.ui.constants import DEFAULT_MIDI_INPUT
from beethoven.ui.managers import AppManager
from beethoven.ui.utils import block_signal


class MidiInputComboBox(QComboBox):
    value_changed = Signal(str)

    def __init__(self, *args, manager: AppManager, **kwargs):
        super(MidiInputComboBox, self).__init__(*args, **kwargs)

        self.manager = manager
        self.value = DEFAULT_MIDI_INPUT

        self.refresh()

        self.currentTextChanged.connect(self.handle_input_name_change)

    def set(self, name: str):
        self.value = name

        with block_signal([self]):
            self.setCurrentText(name)

    def handle_input_name_change(self, name: str):
        self.value = name

        self.value_changed.emit(name)

    def refresh(self):
        with block_signal([self]):
            self.clear()
            self.addItem(DEFAULT_MIDI_INPUT)

            input_names = list(sorted(set(self.manager.adapters.midi.available_inputs)))

            self.addItems(input_names)

            selected_input = self.value or self.manager.settings.midi.selected_input

            if selected_input and selected_input in input_names:
                self.set(selected_input)
            else:
                self.set("")

                self.value_changed.emit(None)
