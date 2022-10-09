from functools import partial

from PySide6.QtCore import Signal

from beethoven.ui.components.buttons import PushPullButton
from beethoven.ui.components.selectors.grid.base import BaseGridSelector
from beethoven.ui.constants import CHORDS_DATA_FLATTEN
from beethoven.ui.layouts import vertical_layout
from beethoven.ui.utils import block_signal


class ChordGridSelector(BaseGridSelector):
    chord_name_changed = Signal(str)

    def __init__(self, *args, grid_width: int, **kwargs):
        super(ChordGridSelector, self).__init__(*args, **kwargs)

        self.buttons = []
        self.chord_name_buttons = {}

        for chord_data in CHORDS_DATA_FLATTEN:
            chord_name = chord_data.short_name

            button = PushPullButton(
                pressed=chord_name,
                released=chord_name,
                state=False,
                object_name="grid_item",
            )
            button.toggled.connect(partial(self.handle_chord_click, button))

            self.buttons.append(button)
            self.chord_name_buttons[chord_name] = button

        layout = vertical_layout(self.format_grid_rows(self.buttons, grid_width))

        self.setLayout(layout)

    def handle_chord_click(self, button, state):
        self.handle_button_states(button, empty_allowed=True)

        self.chord_name_changed.emit(button.text() if state else "")

    def set_chord_name(self, name: str):
        with block_signal(self.buttons):
            if not name:
                self.clear()
            else:
                self.handle_button_states(self.chord_name_buttons[name])
