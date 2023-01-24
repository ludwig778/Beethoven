from typing import List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeWidgetItem

from beethoven.ui.components.selectors.base import BaseSelector
from beethoven.ui.utils import block_signal


class BaseExclusiveSelector(BaseSelector):
    def __init__(
        self,
        *args,
        data,
        labels: List[str],
        expanded_labels: List[str],
        checked: str,
        **kwargs
    ):
        super(BaseExclusiveSelector, self).__init__(*args, **kwargs)

        self.checked_item = None

        for label in labels:
            expanded_state = label in expanded_labels

            item = QTreeWidgetItem([label])

            for sub_data in data.get(label):
                name = self.get_name(sub_data)

                child = QTreeWidgetItem([name] * 2)
                item.addChild(child)

                if name == checked:
                    child.setCheckState(0, Qt.Checked)

                    self.checked_item = child
                else:
                    child.setCheckState(0, Qt.Unchecked)

            self.addTopLevelItem(item)

            item.setExpanded(expanded_state)

        self.itemChanged.connect(self.item_changed)
        self.itemClicked.connect(self.item_clicked)

    def item_clicked(self, item):
        if self.has_item_childrens(item):
            return

        item.setCheckState(0, Qt.Checked)

        self.item_changed(item)

    def item_changed(self, item):
        if self.has_item_childrens(item):
            return

        if self.checked_item == item:
            return

        elif self.checked_item:
            with block_signal([self]):
                self.checked_item.setCheckState(0, Qt.Unchecked)

        self.checked_item = item
