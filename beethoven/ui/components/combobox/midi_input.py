from typing import Optional
from PySide6.QtWidgets import QComboBox

from beethoven.ui.constants import DEFAULT_MIDI_INPUT
from beethoven.ui.managers import AppManager
from beethoven.ui.utils import set_object_name


class MidiInputComboBox(QComboBox):
    def __init__(self, *args, manager: AppManager, value: Optional[str], **kwargs):
        super(MidiInputComboBox, self).__init__(*args, **kwargs)

        set_object_name(self, **kwargs)

        self.manager = manager

        self.setup_items()

        if value:
            self.setCurrentText(value)

    def setup_items(self):
        current_input = self.manager.settings.midi.selected_input

        self.clear()
        self.addItem(DEFAULT_MIDI_INPUT)

        input_names = list(set(sorted(self.manager.adapters.midi.available_inputs)))

        self.addItems(input_names)

        if current_input in input_names:
            self.setCurrentText(current_input)
