import logging
from typing import Dict

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox, QWidget

from beethoven.ui.components.widget_stack import StackedWidget
from beethoven.ui.layouts import Spacing, vertical_layout

logger = logging.getLogger("widget_selector")


class WidgetSelectorComboBox(QWidget):
    value_changed = Signal()

    def __init__(self, *args, widgets: Dict[str, QWidget], parent=None, **kwargs):
        super(WidgetSelectorComboBox, self).__init__(*args, **kwargs)

        self.combobox = QComboBox()
        self.combobox.addItems(list(widgets.keys()))

        self.stack = StackedWidget(widgets=widgets)

        self.combobox.currentIndexChanged.connect(self.handle_widget_change)

        self.setLayout(vertical_layout([self.combobox, Spacing(size=10), self.stack]))

    def setup(self):
        logger.info("setup")

        self.stack.setup()

    def teardown(self):
        logger.info("teardown")

        self.stack.teardown()

    def handle_widget_change(self, index: int):
        self.stack.set_index(index)

        self.value_changed.emit()
