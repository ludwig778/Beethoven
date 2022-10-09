from typing import Tuple

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog

from beethoven.models import Scale
from beethoven.ui.components.buttons import Button
from beethoven.ui.components.chord_picker import ChordPicker
from beethoven.ui.layouts import horizontal_layout, vertical_layout
from beethoven.ui.managers import AppManager
from beethoven.ui.models import ChordItem


class ChordPickerDialog(QDialog):
    chord_item_changed = Signal(ChordItem)

    def __init__(
        self,
        *args,
        manager: AppManager,
        current_chord_item: ChordItem,
        current_scale: Scale,
        **kwargs
    ):
        super(ChordPickerDialog, self).__init__(*args, **kwargs)

        self.widget = ChordPicker(
            manager=manager,
            current_chord_item=current_chord_item,
            current_scale=current_scale,
        )
        self.widget.chord_item_changed.emit(self.chord_item_changed.emit)

        self.ok_button = Button("Ok")
        self.cancel_button = Button("Cancel")

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self.setLayout(
            vertical_layout([
                self.widget,
                horizontal_layout([
                    self.ok_button,
                    self.cancel_button,
                ]),
            ])
        )

    def get_new_chord(self) -> Tuple[bool, ChordItem]:
        return (bool(self.exec_()), self.widget.current_chord_item)
