from functools import partial

from PySide6.QtCore import Signal

from beethoven.models import Degree
from beethoven.ui.components.buttons import PushPullButton
from beethoven.ui.components.selectors.grid.base import BaseGridSelector
from beethoven.ui.constants import DEGREES
from beethoven.ui.layouts import vertical_layout
from beethoven.ui.utils import block_signal


class DegreeGridSelector(BaseGridSelector):
    value_changed = Signal(Degree)

    def __init__(self, *args, grid_width: int, **kwargs):
        super(DegreeGridSelector, self).__init__(*args, **kwargs)

        self.buttons = []
        self.degree_buttons = {}

        for degree in DEGREES:
            degree_name = str(degree)

            button = PushPullButton(degree_name)
            button.toggled.connect(partial(self.handle_root_change, button, degree))

            self.buttons.append(button)
            self.degree_buttons[degree] = button

        self.setLayout(vertical_layout(self.format_grid_rows(self.buttons, grid_width)))

    def set(self, degree: Degree):
        with block_signal(self.buttons):
            self.handle_button_states(self.degree_buttons[Degree(name=degree.name)])

    def handle_root_change(self, button, degree, state):
        self.handle_button_states(button)

        if state:
            self.value_changed.emit(degree)
