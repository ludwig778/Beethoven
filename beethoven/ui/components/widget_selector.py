from typing import Dict

from PySide6.QtWidgets import QComboBox, QWidget

from beethoven.ui.layouts import stacked_layout, vertical_layout
from beethoven.ui.managers.app import AppManager


class ComboBoxSelectedWidget(QWidget):
    def __init__(self, *args, manager: AppManager, widgets: Dict[str, QWidget], **kwargs):
        super(ComboBoxSelectedWidget, self).__init__(*args, **kwargs)

        self.manager = manager

        self.combobox = QComboBox()
        self.combobox.addItems(list(widgets.keys()))

        self.stacked_layout = stacked_layout(list(widgets.values()))

        self.combobox.currentIndexChanged.connect(self.stacked_layout.setCurrentIndex)

        self.setLayout(vertical_layout([self.combobox, self.stacked_layout]))
