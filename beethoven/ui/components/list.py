from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QWidget,
)

from beethoven.ui.layouts import vertical_layout
from beethoven.ui.models import ChordItem, HarmonyItem, HarmonyItems


class BaseListWidget(QListWidget):
    position_altered = Signal()

    def __init__(self, *args, **kwargs):
        super(BaseListWidget, self).__init__(*args, **kwargs)

        self.setSpacing(0)
        self.setFlow(QListWidget.LeftToRight)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setDragDropMode(QAbstractItemView.InternalMove)

        self.model().rowsMoved.connect(lambda: self.position_altered.emit)

    def add_widget_as_item(self, widget):
        item = QListWidgetItem()
        item.setSizeHint(widget.sizeHint())

        row = self.currentRow()

        self.insertItem(row + 1, item)
        self.setItemWidget(item, widget)
        self.setCurrentItem(item)

    def delete_current_item(self):
        if self.count() < 2:
            return

        row = self.currentRow()
        item = self.takeItem(row)
        del item

        new_row = max(0, min(row, self.count() - 1))
        if row != row:
            self.setCurrentRow(new_row)

    def get_current_item_widget(self):
        item = self.currentItem()
        widget = self.itemWidget(item)

        return item, widget


class HarmonyListWidget(BaseListWidget):
    def __init__(self, *args, harmony_items: HarmonyItems, **kwargs):
        super(HarmonyListWidget, self).__init__(*args, **kwargs)

        self.set_harmonies(harmony_items, setup=True)

    def set_harmonies(self, harmony_items: HarmonyItems, **kwargs):
        self.clear()
        self.harmony_items = harmony_items

        for harmony_item in harmony_items.items:
            self.add_item(harmony_item, **kwargs)

        self.setCurrentRow(0)

    def add_item(self, harmony_item: HarmonyItem, setup: bool = False):
        if not setup:
            self.harmony_items.items.insert(self.currentRow() + 1, harmony_item)

        widget = HarmonyListWidgetItem(harmony_item=harmony_item)

        self.add_widget_as_item(widget)

    def get_current_harmony_item(self):
        return self.harmony_items.items[self.currentRow()]

    def update_current_item(self):
        item, widget = self.get_current_item_widget()

        widget.update_labels()

        item.setSizeHint(widget.sizeHint())

    def delete_current_item(self):
        del self.harmony_items.items[self.currentRow()]

        super().delete_current_item()


class ChordListWidget(BaseListWidget):
    def __init__(self, *args, harmony_item: HarmonyItem, **kwargs):
        super(ChordListWidget, self).__init__(*args, **kwargs)

        self.set_chords(harmony_item, setup=True)

    def set_chords(self, harmony_item: HarmonyItem, **kwargs):
        self.clear()
        self.harmony_item = harmony_item

        for chord_item in harmony_item.chord_items:
            self.add_item(chord_item, **kwargs)

        self.setCurrentRow(0)

    def add_item(self, chord_item: ChordItem, setup: bool = False):
        if not setup:
            self.harmony_item.chord_items.insert(self.currentRow() + 1, chord_item)

        widget = ChordListWidgetItem(chord_item=chord_item)

        self.add_widget_as_item(widget)

    def get_current_chord_item(self):
        return self.harmony_item.chord_items[self.currentRow()]

    def update_current_item(self, chord_item: ChordItem):
        item, widget = self.get_current_item_widget()

        self.harmony_item.chord_items[self.currentRow()] = chord_item

        widget.chord_item = chord_item
        widget.update_chord()

        item.setSizeHint(widget.sizeHint())

    def delete_current_item(self):
        del self.harmony_item.chord_items[self.currentRow()]

        super().delete_current_item()


class HarmonyListWidgetItem(QWidget):
    def __init__(self, *args, harmony_item: HarmonyItem, **kwargs):
        super(HarmonyListWidgetItem, self).__init__(*args, **kwargs)

        self.harmony_item = harmony_item

        self.scale_label = QLabel()
        self.progression_label = QLabel()

        self.scale_label.setAlignment(Qt.AlignCenter)  # type: ignore
        self.progression_label.setAlignment(Qt.AlignCenter)  # type: ignore

        self.setLayout(vertical_layout([self.scale_label, self.progression_label]))
        self.update_labels()

    def update_labels(self):
        scale = self.harmony_item.scale

        self.scale_label.setText(str(scale))
        self.progression_label.setText(
            "  \u2794  ".join(
                [str(chord_item) for chord_item in self.harmony_item.chord_items]
            )
        )


class ChordListWidgetItem(QWidget):
    def __init__(self, *args, chord_item: ChordItem, **kwargs):
        super(ChordListWidgetItem, self).__init__(*args, **kwargs)

        self.chord_item = chord_item

        self.chord_label = QLabel()
        self.chord_label.setAlignment(Qt.AlignCenter)  # type: ignore

        self.setLayout(vertical_layout([self.chord_label]))
        self.update_chord()

    def update_chord(self):
        self.chord_label.setText(str(self.chord_item))
