from pathlib import Path
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)

        self.setAttribute(Qt.WA_StyledBackground)


class IconButton(Button):
    def __init__(self, *args, icon_path: Path, **kwargs):
        super(IconButton, self).__init__(*args, **kwargs)

        self.setIcon(QIcon(str(icon_path)))


class PushPullButton(Button):
    def __init__(
        self,
        text: str,
        *args,
        pressed: bool = False,
        pressed_text: Optional[str] = None,
        **kwargs
    ):
        super(PushPullButton, self).__init__(text, *args, **kwargs)

        self.pressed = pressed

        self.released_text = text
        self.pressed_text = pressed_text

        self.clicked.connect(self.toggle)

        if self.pressed:
            self.toggle()

    def toggle(self):
        self.pressed ^= True

        self.setProperty("pressed", self.pressed)

        self.style().unpolish(self)
        self.style().polish(self)

        if self.pressed and self.pressed_text:
            self.setText(self.pressed_text)
        else:
            self.setText(self.released_text)

        self.toggled.emit(self.pressed)

    def release(self):
        if self.pressed:
            self.toggle()


class IconPushPullButton(PushPullButton):
    def __init__(self, *args, icon_path: Path, **kwargs):
        super(IconPushPullButton, self).__init__("", *args, **kwargs)

        self.setIcon(QIcon(str(icon_path)))
