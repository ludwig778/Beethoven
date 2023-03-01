from functools import partial
from typing import Dict, Optional

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from beethoven.models import Note
from beethoven.ui.components.buttons import PushPullButton
from beethoven.ui.constants import ROOTS
from beethoven.ui.layouts import LayoutItems, horizontal_layout
from beethoven.ui.utils import block_signal


class BaseNoteGridSelector(QWidget):
    value_changed = Signal(object)

    def __init__(self, *args, base_note: Optional[Note] = None, **kwargs):
        super(BaseNoteGridSelector, self).__init__(*args, **kwargs)

        self.base_note_buttons: Dict[Note, PushPullButton] = {}
        self._current_button: Optional[PushPullButton] = None

        layout_items: LayoutItems = []

        for _base_note in ROOTS:
            _base_note_name = str(_base_note)

            button = PushPullButton(_base_note_name)
            button.toggled.connect(partial(self.handle_root_change, button, _base_note))

            layout_items.append(button)
            self.base_note_buttons[_base_note] = button

        if base_note:
            self.set(base_note)

        self.setLayout(horizontal_layout(layout_items))

    def set(self, base_note: Optional[Note] = None):
        if base_note is None:
            if self._current_button and self._current_button.pressed:
                with block_signal([self._current_button]):
                    self._current_button.toggle()

            self._current_button = None

            return

        base_note_button = self.base_note_buttons[base_note]

        if self._current_button and self._current_button != base_note_button:
            with block_signal([self._current_button]):
                self._current_button.release()

        if not base_note_button.pressed:
            with block_signal([base_note_button]):
                base_note_button.toggle()

        self._current_button = base_note_button

    def clear(self):
        if self._current_button:
            with block_signal([self._current_button]):
                self._current_button.release()

    def handle_root_change(self, button: PushPullButton, base_note: Note, state: bool):
        if state:
            if self._current_button and self._current_button != button:
                with block_signal([self._current_button]):
                    self._current_button.release()

            self._current_button = button
        else:
            self._current_button = None

        self.value = base_note if state else None

        self.value_changed.emit(self.value)
