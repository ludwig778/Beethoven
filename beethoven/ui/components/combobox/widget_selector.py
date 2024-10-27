import logging
from typing import List, Tuple

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox, QWidget

from beethoven.ui.components.widget_stack import StackedWidget
from beethoven.ui.layouts import (Spacing, Stretch, horizontal_layout,
                                  vertical_layout)

logger = logging.getLogger("widget_selector")


class WidgetSelectorComboBox(QWidget):
    value_changed = Signal()

    def __init__(self, *args, widgets: List[Tuple[str, QWidget]], selected_index: int = 0, **kwargs):
        super(WidgetSelectorComboBox, self).__init__(*args, **kwargs)

        self.combobox = QComboBox()
        # self.combobox.addItems(list(widgets.keys()))
        widget_objects = []
        for widget_name, widget_object in widgets:
            self.combobox.addItem(widget_name)
            widget_objects.append(widget_object)

        self.stack = StackedWidget(widgets=widget_objects)

        self.combobox.currentIndexChanged.connect(self.handle_widget_change)

        self.setLayout(
            vertical_layout(
                [
                    Spacing(size=5),
                    horizontal_layout(
                        [
                            Stretch(),
                            self.combobox,
                            Stretch(),
                        ]
                    ),
                    Spacing(size=5),
                    self.stack,
                ]
            )
        )

    def setup(self):
        logger.info("setup")

        self.stack.setup()

    def teardown(self):
        logger.info("teardown")

        self.stack.teardown()

    def handle_widget_change(self, index: int):
        self.stack.set_index(index)

        self.value_changed.emit()
