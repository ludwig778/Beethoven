from functools import partial

from PySide6.QtCore import Signal

from beethoven.models import Note
from beethoven.ui.components.buttons import PushPullButton
from beethoven.ui.components.selectors.grid.base import BaseGridSelector
from beethoven.ui.constants import ROOTS
from beethoven.ui.layouts import vertical_layout
from beethoven.ui.utils import block_signal


class RootGridSelector(BaseGridSelector):
    root_changed = Signal(Note)

    def __init__(self, *args, grid_width: int, **kwargs):
        super(RootGridSelector, self).__init__(*args, **kwargs)

        self.buttons = []
        self.root_buttons = {}

        for root in ROOTS:
            root_name = str(root)

            button = PushPullButton(
                pressed=root_name,
                released=root_name,
                state=False,
                object_name="grid_item",
            )
            button.toggled.connect(partial(self.handle_root_click, button, root))

            self.buttons.append(button)
            self.root_buttons[root] = button

        layout = vertical_layout(self.format_grid_rows(self.buttons, grid_width))
        layout.setSpacing(0)

        self.setLayout(layout)

    def handle_root_click(self, button, root, state):
        self.handle_button_states(button)

        if state:
            self.root_changed.emit(root)

    def set_root(self, root: Note):
        with block_signal(self.buttons):
            self.handle_button_states(self.root_buttons[root])
