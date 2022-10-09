from typing import List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeWidgetItem

from beethoven.ui.components.selectors.base import BaseSelector


class MultipleSelector(BaseSelector):
    def __init__(
        self,
        *args,
        data,
        labels: List[str],
        expanded_labels: List[str],
        checked_labels: List[str],
        **kwargs
    ):
        super(MultipleSelector, self).__init__(*args, **kwargs)

        for label in labels:
            expanded_state = label in expanded_labels
            checked_state = Qt.Checked if label in checked_labels else Qt.Unchecked

            item = QTreeWidgetItem([label])

            for sub_data in data.get(label):
                name = self.get_name(sub_data)

                child = QTreeWidgetItem([name] * 2)
                child.setCheckState(0, checked_state)
                item.addChild(child)

            self.addTopLevelItem(item)

            item.setCheckState(0, checked_state)
            item.setExpanded(expanded_state)

        self.itemChanged.connect(self.item_changed)

    def item_changed(self, item):
        is_top_level = item.childCount() != 0

        if not is_top_level:
            return

        checked_state = item.checkState(0)

        for child_level_index in range(item.childCount()):
            child = item.child(child_level_index)
            child.setCheckState(0, checked_state)

        if checked_state == Qt.Checked and not item.isExpanded():
            item.setExpanded(True)
        elif checked_state == Qt.Unchecked and item.isExpanded():
            item.setExpanded(False)
