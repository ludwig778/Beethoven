from functools import partial
from typing import Dict, List, Set

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from beethoven.models import Interval
from beethoven.ui.components.buttons import PushPullButton
from beethoven.ui.layouts import LayoutItems, horizontal_layout
from beethoven.ui.utils import block_signal


class ExtensionsGridSelector(QWidget):
    value_changed = Signal(object)

    def __init__(self, *args, extensions: List[Interval] | None, **kwargs):
        super(ExtensionsGridSelector, self).__init__(*args, **kwargs)

        self._values: Set[Interval] = set()

        self.extension_buttons: Dict[Interval, PushPullButton] = {}
        self._current_buttons: Set[PushPullButton] = set()

        layout_items: LayoutItems = []

        extension_names = [
            "8",
            "9m",
            "9",
            "10m",
            "10",
            "11",
            "11a",
            "12",
            "13m",
            "13",
            "14m",
            "14",
        ]

        for extension_name in extension_names:
            extension = Interval.parse(extension_name)

            button = PushPullButton(extension.extension_str())
            button.toggled.connect(partial(self.handle_chord_change, button, extension))

            self.extension_buttons[extension] = button

            layout_items.append(button)

        self.set(extensions)

        self.setLayout(horizontal_layout(layout_items))

    @property
    def value(self) -> List[Interval] | None:
        return list(sorted(self._values)) if self._values else None

    def set(self, extensions: List[Interval] | None):
        self._values = set(extensions) if extensions else set()

        new_buttons = set()

        for extension in self._values:
            extension_button = self.extension_buttons[extension]

            new_buttons.add(extension_button)

        for button in list(self._current_buttons):
            if button not in new_buttons:
                with block_signal([button]):
                    button.toggle()

        for button in new_buttons:
            if button not in self._current_buttons:
                with block_signal([button]):
                    button.toggle()

        self._current_buttons = new_buttons

    def handle_chord_change(self, button: PushPullButton, extension: Interval, state: bool):
        if state:
            self._current_buttons.add(button)
            self._values.add(extension)
        elif button in self._current_buttons:
            self._current_buttons.remove(button)
            self._values.remove(extension)

        self.value_changed.emit(self.value)
