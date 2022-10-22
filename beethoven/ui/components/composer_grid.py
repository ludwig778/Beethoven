from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from beethoven.models.scale import Scale
from beethoven.ui.components.buttons import Button
from beethoven.ui.components.list import ChordListWidget, HarmonyListWidget
from beethoven.ui.layouts import horizontal_layout, vertical_layout
from beethoven.ui.managers import AppManager
from beethoven.ui.models import ChordItem, HarmonyItem, HarmonyItems
from beethoven.ui.sizing import VerticalExplandPolicy, set_size_policies
from beethoven.ui.utils import (
    block_signal,
    get_default_chord_item,
    get_default_harmony_item,
)


class HarmonyGridWidget(QWidget):
    item_changed = Signal(HarmonyItem)
    current_item_deleted = Signal()

    def __init__(
        self, *args, manager: AppManager, harmony_items: HarmonyItems, **kwargs
    ):
        super(HarmonyGridWidget, self).__init__(*args, **kwargs)

        self.manager = manager
        self.harmony_items = harmony_items

        self.add_button = Button("Add")
        self.delete_button = Button("Delete")

        self.list = HarmonyListWidget(harmony_items=harmony_items)

        self.add_button.clicked.connect(self.add_item)
        self.delete_button.clicked.connect(self.delete_current_item)

        self.list.currentItemChanged.connect(self.current_item_changed)

        self.setFixedHeight(90)

        self.add_button.setFixedWidth(70)
        self.delete_button.setFixedWidth(70)

        set_size_policies(
            [
                self.list,
                self.add_button,
                self.delete_button,
            ],
            VerticalExplandPolicy,
        )

        self.setLayout(
            horizontal_layout(
                [
                    self.list,
                    vertical_layout(
                        [
                            self.add_button,
                            self.delete_button,
                        ]
                    ),
                ]
            ),
        )

    def add_item(self):
        self.list.add_item(get_default_harmony_item())

    def current_item_changed(self):
        self.item_changed.emit(self.get_current_item())

    def update_current_item(self, scale: Scale):
        harmony_item = self.list.get_current_harmony_item()
        harmony_item.scale = scale

        self.list.update_current_item()

    def delete_current_item(self):
        if len(self) > 1:
            with block_signal([self.list]):
                self.list.delete_current_item()

                self.current_item_deleted.emit()

    def set_current_item_index(self, index: int):
        self.list.setCurrentRow(index)

    def get_current_item_index(self):
        return self.list.currentRow()

    def get_current_item(self):
        return self.harmony_items.items[self.get_current_item_index()]

    def update_current_item_display(self):
        self.list.update_current_item()

    def is_current_item_last(self):
        return self.get_current_item_index() + 1 >= len(self)

    def next(self):
        items_len = len(self)
        next_item_index = self.get_current_item_index() + 1

        self.set_current_item_index(next_item_index if next_item_index < items_len else 0)

    def __len__(self):
        return self.list.count()


class ChordGridWidget(QWidget):
    item_added = Signal()
    item_changed = Signal(HarmonyItem)
    current_item_deleted = Signal()

    def __init__(
        self, *args, manager: AppManager, harmony_item: HarmonyItem, **kwargs
    ):
        super(ChordGridWidget, self).__init__(*args, **kwargs)

        self.manager = manager
        self.harmony_item = harmony_item

        self.add_button = Button("Add")
        self.delete_button = Button("Delete")

        self.list = ChordListWidget(harmony_item=harmony_item)

        self.add_button.clicked.connect(self.add_item)
        self.delete_button.clicked.connect(self.delete_current_item)

        self.list.currentItemChanged.connect(self.current_item_changed)

        self.setFixedHeight(55)

        self.add_button.setFixedWidth(70)
        self.delete_button.setFixedWidth(70)

        set_size_policies(
            [
                self.list,
                self.add_button,
                self.delete_button,
            ],
            VerticalExplandPolicy,
        )

        self.setLayout(
            horizontal_layout(
                [
                    self.list,
                    vertical_layout(
                        [
                            self.add_button,
                            self.delete_button,
                        ]
                    ),
                ]
            ),
        )

    def add_item(self):
        self.list.add_item(get_default_chord_item())

        self.item_added.emit()

    def set_items(self, harmony_item: HarmonyItem, **kwargs):
        self.harmony_item = harmony_item

        with block_signal([self.list]):
            self.list.set_chords(harmony_item, **kwargs)

    def current_item_changed(self):
        self.item_changed.emit(self.get_current_item())

    def update_current_item(self, chord_item: ChordItem):
        self.list.update_current_item(chord_item)

    def delete_current_item(self):
        with block_signal([self.list]):
            self.list.delete_current_item()

            self.current_item_deleted.emit()

    def set_current_item_index(self, index: int):
        self.list.setCurrentRow(index)

    def get_current_item_index(self):
        return self.list.currentRow()

    def get_current_item(self):
        return self.harmony_item.chord_items[self.get_current_item_index()]

    def update_current_item_display(self):
        self.list.update_current_item()

    def is_current_item_last(self):
        return self.get_current_item_index() + 1 >= len(self)

    def next(self):
        items_len = len(self)
        next_item_index = self.get_current_item_index() + 1

        self.set_current_item_index(next_item_index if next_item_index < items_len else 0)

    def __len__(self):
        return self.list.count()


class ComposerGrid(QWidget):
    harmony_item_changed = Signal(HarmonyItem, ChordItem)
    chord_item_changed = Signal(ChordItem)

    def __init__(
        self, *args, manager: AppManager, harmony_items: HarmonyItems, **kwargs
    ):
        super(ComposerGrid, self).__init__(*args, **kwargs)

        self.manager = manager
        self.harmony_items = harmony_items

        self.harmony_grid = HarmonyGridWidget(
            manager=manager,
            harmony_items=harmony_items
        )
        self.chord_grid = ChordGridWidget(
            manager=manager,
            harmony_item=harmony_items.items[0]
        )

        self.harmony_grid.item_changed.connect(self.update_chords_list)

        self.chord_grid.item_added.connect(self.harmony_grid.update_current_item_display)
        self.chord_grid.current_item_deleted.connect(self.harmony_grid.update_current_item_display)

        self.setFixedHeight(160)
        self.setMinimumWidth(350)

        self.setLayout(vertical_layout([self.harmony_grid, self.chord_grid]))

    def next(self):
        if not self.chord_grid.is_current_item_last():
            self.chord_grid.next()

        else:
            if self.harmony_grid.is_current_item_last():
                self.harmony_grid.next()
            else:
                self.chord_grid.set_current_item_index(0)
                self.harmony_grid.set_current_item_index(0)

    def get_current_item(self):
        return (
            self.harmony_grid.get_current_item(),
            self.chord_grid.get_current_item(),
        )

    def update_chord(self):
        self.chord_item_changed.emit(self.chord_grid.get_current_item())

    def update_chords_list(self):
        harmony_item = self.harmony_grid.get_current_item()

        self.chord_grid.set_items(harmony_item, setup=True)

        self.harmony_item_changed.emit(
            self.harmony_grid.get_current_item(),
            self.chord_grid.get_current_item(),
        )

    def update_current_chord(self, chord_item: ChordItem):
        self.chord_grid.update_current_item(chord_item)
        self.harmony_grid.update_current_item_display()
