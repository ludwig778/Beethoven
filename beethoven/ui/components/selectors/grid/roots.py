from functools import partial
from typing import Dict, Optional

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from beethoven.models import Note
from beethoven.ui.components.buttons import PushPullButton
from beethoven.ui.constants import ROOTS
from beethoven.ui.layouts import LayoutItems, horizontal_layout
from beethoven.ui.utils import block_signal


class RootGridSelector(QWidget):
    value_changed = Signal(Note)

    def __init__(self, *args, root: Optional[Note] = None, **kwargs):
        super(RootGridSelector, self).__init__(*args, **kwargs)

        self.root_buttons: Dict[Note, PushPullButton] = {}
        self._current_button: Optional[PushPullButton] = None

        layout_items: LayoutItems = []

        for _root in ROOTS:
            root_name = str(_root)

            button = PushPullButton(root_name)
            button.toggled.connect(partial(self.handle_root_change, button, _root))

            layout_items.append(button)
            self.root_buttons[_root] = button

        if root:
            self.set(root)

        self.setLayout(horizontal_layout(layout_items))

    def set(self, root: Note):
        root_button = self.root_buttons[root]

        if self._current_button and self._current_button != root_button:
            with block_signal([self._current_button]):
                self._current_button.release()

        if not root_button.pressed:
            with block_signal([root_button]):
                root_button.toggle()

        self._current_button = root_button

    def clear(self):
        if self._current_button:
            with block_signal([self._current_button]):
                self._current_button.release()

    def handle_root_change(self, button, root, state):
        if state:
            if self._current_button and self._current_button.pressed:
                with block_signal([self._current_button]):
                    self._current_button.release()

            self._current_button = button

            self.value = root if state else None

            self.value_changed.emit(self.value)
        else:
            if self._current_button == button:
                with block_signal([self._current_button]):
                    self._current_button.toggle()
