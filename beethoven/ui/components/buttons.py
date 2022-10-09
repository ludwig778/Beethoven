from typing import Optional

from PySide6.QtWidgets import QPushButton


class Button(QPushButton):
    def __init__(self, *args, object_name: Optional[str] = None, **kwargs):
        super(Button, self).__init__(*args, **kwargs)

        if object_name:
            self.setObjectName(object_name)


class PushPullButton(Button):
    def __init__(self, *args, pressed: str, released: str, state: bool, **kwargs):
        super(PushPullButton, self).__init__(*args, **kwargs)

        self.setCheckable(True)
        self.setChecked(state)

        self.state = state
        self.pressed = pressed
        self.released = released

        self.toggled.connect(self.toggle_button)

        self.update_text()

    @property
    def is_pressed(self):
        return self.state

    def release(self):
        self.setChecked(False)

        if self.state:
            self.toggle_button(not self.state)

    def toggle_button(self, new_state):
        self.state = new_state

        self.update_text()

    def update_text(self):
        self.setText(self.pressed if self.state else self.released)
