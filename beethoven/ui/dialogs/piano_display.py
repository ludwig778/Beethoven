import logging

from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QDialog

from beethoven.ui.components.piano_display import PianoDisplay
from beethoven.ui.layouts import Stretch, vertical_layout

logger = logging.getLogger("dialog.display_piano")


class PianoDisplayDialog(QDialog):
    def __init__(self, *args, harmony_item, chord_item, **kwargs):
        super(PianoDisplayDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("Piano Display")

        self.graphic = PianoDisplay(harmony_item=harmony_item, chord_item=chord_item)

        self.action_binding = QShortcut(QKeySequence("q"), self)
        self.action_binding.activated.connect(self.close)  # type: ignore

        self.update_items = self.graphic.update_items

        self.setLayout(vertical_layout([self.graphic, Stretch()], margins=(5,) * 4))
