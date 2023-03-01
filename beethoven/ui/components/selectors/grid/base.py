from math import ceil
from typing import List

from PySide6.QtWidgets import QWidget

from beethoven.ui.components.buttons import PushPullButton
from beethoven.ui.layouts import horizontal_layout
from beethoven.ui.utils import block_signal


class BaseGridSelector(QWidget):
    buttons: List[PushPullButton]

    def __init__(self, *args, **kwargs):
        super(BaseGridSelector, self).__init__(*args, **kwargs)

    def get_enabled_buttons(self):
        return list(filter(lambda button: button.pressed, self.buttons))

    @staticmethod
    def format_grid_rows(objects, num):
        layouts = []

        for i in range(ceil(len(objects) / num)):
            layouts.append(horizontal_layout(objects[i * num : (i + 1) * num]))

        return layouts

    def clear(self):
        for button in self.buttons:
            if not button.pressed:
                continue

            with block_signal([button]):
                button.toggle()

    def handle_button_states(self, updated_button, empty_allowed=False):
        enabled_buttons = self.get_enabled_buttons()

        if not enabled_buttons and not empty_allowed:
            with block_signal([updated_button]):
                updated_button.toggle()

        else:
            if updated_button in enabled_buttons:
                enabled_buttons.remove(updated_button)

            for enabled_button in enabled_buttons:
                with block_signal([enabled_button]):
                    enabled_button.toggle()
