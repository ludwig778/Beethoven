from typing import Optional
from PySide6.QtWidgets import QComboBox

from beethoven.ui.constants import DEFAULT_MIDI_OUTPUT
from beethoven.ui.managers import AppManager
from beethoven.ui.utils import set_object_name


class MidiOutputComboBox(QComboBox):
    def __init__(self, *args, manager: AppManager, value: Optional[str], **kwargs):
        super(MidiOutputComboBox, self).__init__(*args, **kwargs)

        set_object_name(self, **kwargs)

        self.manager = manager

        self.setup_items()

        if value:
            self.setCurrentText(value)

    def setup_items(self):
        self.addItem(DEFAULT_MIDI_OUTPUT)

        output_names = list(set(sorted(self.manager.adapters.midi.outputs)))

        self.addItems(output_names)
