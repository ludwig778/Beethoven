from functools import partial
from typing import Dict

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from beethoven.models import Degree
from beethoven.ui.components.buttons import PushPullButton
from beethoven.ui.constants import DEGREES
from beethoven.ui.layouts import LayoutItems, horizontal_layout
from beethoven.ui.utils import block_signal


class DegreeGridSelector(QWidget):
    value_changed = Signal(Degree)

    def __init__(self, *args, degree: Degree | None = None, **kwargs):
        super(DegreeGridSelector, self).__init__(*args, **kwargs)

        self.degree_buttons: Dict[Degree, PushPullButton] = {}
        self._current_button: PushPullButton | None = None

        layout_items: LayoutItems = []

        for _degree in DEGREES:
            degree_name = str(_degree)

            button = PushPullButton(degree_name)

            if degree == _degree:
                button.toggle()

            button.toggled.connect(partial(self.handle_root_change, button, _degree))

            layout_items.append(button)
            self.degree_buttons[_degree] = button

        if degree:
            self.set(degree)

        self.setLayout(horizontal_layout(layout_items))

    def set(self, degree: Degree):
        degree = degree.remove_alteration()

        degree_button = self.degree_buttons[degree]

        if self._current_button and self._current_button != degree_button:
            with block_signal([self._current_button]):
                self._current_button.release()

        if not degree_button.pressed:
            with block_signal([degree_button]):
                degree_button.toggle()

        self._current_button = degree_button

    def clear(self):
        if self._current_button:
            with block_signal([self._current_button]):
                self._current_button.release()

    def handle_root_change(self, button, degree, state):
        if state:
            if self._current_button and self._current_button.pressed:
                with block_signal([self._current_button]):
                    self._current_button.release()

            self._current_button = button

            self.value = degree if state else None

            self.value_changed.emit(self.value)
        else:
            if self._current_button == button:
                with block_signal([self._current_button]):
                    self._current_button.toggle()
