from typing import Any, List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem

from beethoven.indexes.models import IndexDataModels, ScaleData


class BaseSelector(QTreeWidget):
    def __init__(self, *args, **kwargs):
        super(BaseSelector, self).__init__(*args, **kwargs)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setHeaderHidden(True)

    @staticmethod
    def has_item_childrens(item: QTreeWidgetItem) -> bool:
        return bool(item.childCount())

    def get_checked_items(self) -> List[QTreeWidgetItem]:
        checked_items = []

        for top_level_index in range(self.topLevelItemCount()):
            top_item = self.topLevelItem(top_level_index)

            for child_level_index in range(top_item.childCount()):
                child_item = top_item.child(child_level_index)

                if child_item.checkState(0) == Qt.Unchecked:
                    continue

                checked_items.append(top_item.child(child_level_index))

        return checked_items

    def get_checked_texts(self) -> List[str]:
        return [item.text(0) for item in self.get_checked_items()]

    @staticmethod
    def get_name(obj: Any) -> str:
        if isinstance(obj, ScaleData):
            return obj.names[0]
        elif isinstance(obj, IndexDataModels):
            return obj.names[0]

        return str(obj)
