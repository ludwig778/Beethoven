import logging
from typing import Dict

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from beethoven.ui.layouts import stacked_layout

logger = logging.getLogger("stacked_widget")


class StackedWidget(QWidget):
    value_changed = Signal()

    def __init__(self, *args, widgets: Dict[str, QWidget], **kwargs):
        super(StackedWidget, self).__init__(*args, **kwargs)

        self.stacked_layout = stacked_layout(list(widgets.values()))

        self.setLayout(self.stacked_layout)

    def setup(self):
        logger.info("setup")

        self.current_widget.setup()

    def teardown(self):
        logger.info("teardown")

        self.current_widget.teardown()

    @property
    def index(self):
        return self.stacked_layout.currentIndex()

    @property
    def current_widget(self):
        return self.stacked_layout.currentWidget()

    def set_index(self, index: int):
        if index != self.index:
            self.current_widget.teardown()

            self.stacked_layout.setCurrentIndex(index)

            self.current_widget.setup()
