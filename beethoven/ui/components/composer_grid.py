import logging
from typing import Callable, Tuple

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QAbstractItemView, QListView,
                               QStyledItemDelegate, QWidget)

from beethoven.models import ChordItem, HarmonyItem
from beethoven.sequencer.objects import HarmonyItemSelector
from beethoven.ui.components.buttons import IconButton, IconPushPullButton
from beethoven.ui.components.list import (ChordDelegate, HarmonyDelegate,
                                          ItemsModel)
from beethoven.ui.layouts import Spacing, horizontal_layout, vertical_layout
from beethoven.ui.utils import (block_signal, get_default_chord_item,
                                get_default_harmony_item, resource_path)

logger = logging.getLogger("composer_grid")


class BaseGrid(QWidget):
    item_added = Signal(object)
    item_clicked = Signal(object)
    item_deleted = Signal(object, object)

    default_item_callable: Callable
    delegate: QStyledItemDelegate

    def setup_list_view(self, obj):
        self.model = ItemsModel(obj)
        self.current_index = self.model.index(0)

        self.list = QListView(self)
        self.list.setModel(self.model)

        self.list.setFlow(QListView.LeftToRight)
        self.list.setItemDelegate(self.delegate)
        self.list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list.setCurrentIndex(self.current_index)
        self.list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.list.selectionModel().selectionChanged.connect(self.handle_item_change)
        self.list.clicked.connect(self.handle_item_click)

    def add_item(self):
        item = self.get_default_item()

        row = self.current_index.row() + 1

        self.model.insert_item(item, row)
        self.current_index = self.model.index(row)
        self.list.setCurrentIndex(self.current_index)

        self.item_added.emit(item)

    @property
    def current_item(self):
        return self.current_index.data()

    def delete_item(self):
        if len(self.model) > 1:
            with block_signal([self.list]):
                row = self.current_index.row()

                print("-" * 33)
                print("-" * 33, "row= ", row)
                print("-" * 33)

                item = self.current_item

                self.model.remove(self.current_index)

                if row == len(self.model):
                    row -= 1

                self.current_index = self.model.index(row)
                self.list.setCurrentIndex(self.current_index)

                self.item_deleted.emit(item, self.current_index.data())

    # Handle click on empty list space
    def handle_item_click(self, item):
        self.current_index = item
        self.item_clicked.emit(self.current_item)

    def handle_item_change(self, selected, *args, **kwargs):
        if not len(selected.indexes()):
            self.list.setCurrentIndex(self.current_index)

    def set_current_item(self, item):
        self.current_index = self.model.index(self.model.items.index(item))

        self.list.setCurrentIndex(self.current_index)

    def set_items(self, items):
        self.model.set_items(items)

    def refresh_current_index(self):
        self.list.dataChanged(self.current_index, self.current_index)


class HarmonyGrid(BaseGrid):
    item_added = Signal(HarmonyItem)
    item_clicked = Signal(HarmonyItem)
    item_deleted = Signal(HarmonyItem, HarmonyItem)

    delegate = HarmonyDelegate()

    def __init__(self, *args, harmony_iterator: HarmonyItemSelector, **kwargs):
        super(HarmonyGrid, self).__init__(*args, **kwargs)

        self.harmony_iterator = harmony_iterator

        self.setFixedHeight(82)
        self.setAttribute(Qt.WA_StyledBackground)

        self.add_button = IconButton(icon_path=resource_path("img/plus-32.png"), object_name="green")
        self.delete_button = IconButton(icon_path=resource_path("img/minus-7-32.png"), object_name="red")

        self.setup_list_view(self.harmony_iterator.harmony_items)
        self.list.setFixedHeight(82)

        self.add_button.clicked.connect(self.add_item)
        self.delete_button.clicked.connect(self.delete_item)

        self.setLayout(
            horizontal_layout([
                self.list,
                vertical_layout([self.add_button, self.delete_button]),
            ]),
        )

    def get_default_item(self):
        return get_default_harmony_item()


class ChordGrid(BaseGrid):
    item_added = Signal(ChordItem)
    item_clicked = Signal(ChordItem)
    item_deleted = Signal(ChordItem, ChordItem)

    delegate = ChordDelegate()

    # def __init__(self, *args, chord_items: List[ChordItem], **kwargs):
    def __init__(self, *args, harmony_iterator: HarmonyItemSelector, **kwargs):
        super(ChordGrid, self).__init__(*args, **kwargs)

        self.harmony_iterator = harmony_iterator

        self.setFixedHeight(50)
        self.setAttribute(Qt.WA_StyledBackground)

        self.add_button = IconButton(icon_path=resource_path("img/plus-32.png"), object_name="green")
        self.delete_button = IconButton(icon_path=resource_path("img/minus-7-32.png"), object_name="red")
        self.modify_button = IconPushPullButton(
            icon_path=resource_path("img/gear-32.png"), object_name="blue"
        )

        self.setup_list_view(self.harmony_iterator.current_harmony_item.chord_items)
        self.list.setFixedHeight(50)

        self.add_button.clicked.connect(self.add_item)
        self.delete_button.clicked.connect(self.delete_item)

        self.setLayout(
            horizontal_layout(
                [
                    self.list,
                    self.add_button,
                    self.delete_button,
                    self.modify_button,
                ]
            ),
        )

    def set_first_item_as_current_item(self) -> int:
        row = 0

        self.harmony_iterator.chord_index = row

        self.current_index = self.model.index(row)
        self.list.setCurrentIndex(self.current_index)

        return row

    def get_default_item(self):
        return get_default_chord_item()

    def update_chord_item(self, chord_item: ChordItem):
        self.model.setData(self.current_index, chord_item)

        self.refresh_current_index()


class ComposerGrid(QWidget):
    items_changed = Signal(HarmonyItem, ChordItem, bool)

    def __init__(self, *args, harmony_iterator: HarmonyItemSelector, **kwargs):
        super(ComposerGrid, self).__init__(*args, **kwargs)

        self.harmony_iterator = harmony_iterator

        self.harmony_grid = HarmonyGrid(harmony_iterator=self.harmony_iterator)
        self.harmony_grid.item_clicked.connect(self.handle_harmony_item_click)
        self.harmony_grid.item_added.connect(self.handle_harmony_item_deleted)
        self.harmony_grid.item_deleted.connect(self.handle_harmony_item_deleted)

        self.chord_grid = ChordGrid(harmony_iterator=self.harmony_iterator)
        self.chord_grid.item_clicked.connect(self.handle_chord_item_click)
        self.chord_grid.item_added.connect(self.handle_chord_item_added)
        self.chord_grid.item_deleted.connect(self.handle_chord_item_deleted)

        self.setLayout(vertical_layout([self.harmony_grid, Spacing(size=4), self.chord_grid]))

    def handle_harmony_item_click(self, harmony_item):
        self.refresh_chords_list(harmony_item)

        with block_signal([self.chord_grid]):
            self.chord_grid.set_first_item_as_current_item()

        harmony_index = self.harmony_iterator.harmony_items.index(harmony_item)
        self.harmony_iterator.harmony_index = harmony_index

        self.items_changed.emit(harmony_item, harmony_item.chord_items[0], True)

    def handle_harmony_item_added(self, harmony_item):
        self.refresh_chords_list(harmony_item)

        self.chord_grid.set_first_item_as_current_item()

        self.items_changed.emit(harmony_item, harmony_item.chord_items[0], True)

    def handle_harmony_item_deleted(self, *args):
        harmony_item = self.harmony_grid.current_item

        self.refresh_chords_list(harmony_item)
        self.chord_grid.set_first_item_as_current_item()

        harmony_index = self.harmony_iterator.harmony_items.index(harmony_item)

        self.harmony_iterator.harmony_index = harmony_index

        self.items_changed.emit(harmony_item, harmony_item.chord_items[0], True)

    def handle_chord_item_click(self, chord_item: ChordItem):
        chord_index = self.harmony_iterator.current_harmony_item.chord_items.index(chord_item)

        self.harmony_iterator.chord_index = chord_index

        self.items_changed.emit(self.harmony_iterator.current_harmony_item, chord_item, False)

    def handle_chord_item_added(self, chord_item):
        self.items_changed.emit(*(*self.harmony_iterator.current_items, True))
        self.harmony_grid.refresh_current_index()

    def handle_chord_item_deleted(self, *args):
        if self.harmony_iterator.chord_index >= len(self.harmony_grid.current_item.chord_items):
            self.harmony_iterator.chord_index -= 1

        self.items_changed.emit(*(*self.harmony_iterator.current_items, True))
        self.harmony_grid.refresh_current_index()

    def refresh_chords_list(self, harmony_item):
        self.chord_grid.set_items(harmony_item.chord_items)

    def set_current_items(self, harmony_item: HarmonyItem, chord_item: ChordItem):
        """
        print("|- SET GRID")
        print("|", self.harmony_grid.current_item.to_log_string())
        print("|", harmony_item.to_log_string())
        print("|", self.chord_grid.current_item.to_log_string())
        print("|", chord_item.to_log_string())
        """
        self.harmony_grid.set_items(self.harmony_iterator.harmony_items)
        self.harmony_grid.set_current_item(harmony_item)

        self.refresh_chords_list(harmony_item)

        self.chord_grid.set_current_item(chord_item)

    def get_current_items(self) -> Tuple[HarmonyItem, ChordItem]:
        return self.harmony_iterator.current_items
