from functools import partial

from PySide6.QtCore import Signal

from beethoven.models import Note
from beethoven.ui.components.buttons import PushPullButton
from beethoven.ui.components.selectors.grid.base import BaseGridSelector
from beethoven.ui.constants import ROOTS
from beethoven.ui.layouts import vertical_layout
from beethoven.ui.utils import block_signal


class RootGridSelector(BaseGridSelector):
    value_changed = Signal(Note)

    def __init__(self, *args, grid_width: int, **kwargs):
        super(RootGridSelector, self).__init__(*args, **kwargs)

        self.buttons = []
        self.root_buttons = {}

        for root in ROOTS:
            root_name = str(root)

            button = PushPullButton(root_name)
            button.toggled.connect(partial(self.handle_root_change, button, root))

            self.buttons.append(button)
            self.root_buttons[root] = button

        layout = vertical_layout(self.format_grid_rows(self.buttons, grid_width))

        self.setLayout(layout)

    def handle_root_change(self, button, root, state):
        self.handle_button_states(button)

        self.value = root

        if state:
            self.value_changed.emit(self.value)

    def set(self, root: Note):
        with block_signal(self.buttons):
            self.handle_button_states(self.root_buttons[root])
