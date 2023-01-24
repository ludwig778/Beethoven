from typing import Dict

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from beethoven.ui.layouts import stacked_layout


class StackedWidget(QWidget):
    value_changed = Signal()

    def __init__(self, *args, widgets: Dict[str, QWidget], parent=None, **kwargs):
        super(StackedWidget, self).__init__(*args, **kwargs)

        self.stacked_layout = stacked_layout(list(widgets.values()))

        self.setLayout(self.stacked_layout)

    @property
    def index(self):
        return self.stacked_layout.currentIndex()

    def set_index(self, index: int):
        return self.stacked_layout.setCurrentIndex(index)
