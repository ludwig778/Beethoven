import logging
from typing import List

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from beethoven.ui.layouts import stacked_layout

logger = logging.getLogger("stacked_widget")


class StackedWidget(QWidget):
    value_changed = Signal()

    def __init__(self, *args, widgets: List[QWidget], **kwargs) -> None:
        super(StackedWidget, self).__init__(*args, **kwargs)

        self.stacked_layout = stacked_layout(widgets)

        self.setLayout(self.stacked_layout)

    def setup(self) -> None:
        logger.info("setup")

        self.current_widget.setup()

    def teardown(self) -> None:
        logger.info("teardown")

        self.current_widget.teardown()

    @property
    def index(self) -> int:
        return self.stacked_layout.currentIndex()

    @property
    def current_widget(self) -> QWidget:
        return self.stacked_layout.currentWidget()

    def set_index(self, index: int) -> None:
        if index != self.index:
            self.current_widget.teardown()

            self.stacked_layout.setCurrentIndex(index)

            self.current_widget.setup()
