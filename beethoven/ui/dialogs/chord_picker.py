from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QDialog

from beethoven.models import ChordItem
from beethoven.ui.components.chord_picker import ChordPicker
from beethoven.ui.layouts import vertical_layout


class ChordPickerDialog(QDialog):
    value_changed = Signal(ChordItem)

    def __init__(self, *args, chord_item: ChordItem, **kwargs):
        super(ChordPickerDialog, self).__init__(*args, **kwargs)

        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.picker = ChordPicker(chord_item=chord_item, **kwargs)
        self.picker.value_changed.connect(self.value_changed.emit)

        self.setLayout(
            vertical_layout(
                [self.picker],
                margins=(10, 10, 10, 0),
            )
        )

    def set(self, chord_item: ChordItem):
        self.picker.set(chord_item)
