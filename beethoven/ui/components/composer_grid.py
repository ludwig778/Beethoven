from pathlib import Path
from typing import Callable, List, Tuple

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QAbstractItemView, QListView, QStyledItemDelegate, QWidget

from beethoven.models import Bpm, Scale, TimeSignature
from beethoven.ui.components.buttons import IconButton, IconPushPullButton
from beethoven.ui.components.list import ChordDelegate, HarmonyDelegate, ItemsModel
from beethoven.ui.layouts import Spacing, horizontal_layout, vertical_layout
from beethoven.ui.models import ChordItem, HarmonyItem
from beethoven.ui.utils import (
    block_signal,
    get_default_chord_item,
    get_default_harmony_item,
)


class BaseGrid(QWidget):
    item_added = Signal(object)
    item_changed = Signal(object)
    item_clicked = Signal(object)
    item_deleted = Signal(object)

    default_item_callable: Callable
    delegate: QStyledItemDelegate

    def setup_list_view(self, model):
        self.model = model
        self.current_index = self.model.index(0)

        self.list = QListView()
        self.list.setModel(self.model)

        self.list.setFlow(QListView.LeftToRight)
        self.list.setItemDelegate(self.delegate)
        self.list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list.setCurrentIndex(self.current_index)
        self.list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.list.selectionModel().selectionChanged.connect(self.handle_item_change)
        self.list.clicked.connect(self.handle_item_click)

    def add_item(self):
        row = self.current_index.row()

        item = self.get_default_item()

        self.model.insert_item(item, row + 1)

        self.current_index = self.model.index(row + 1)
        self.list.setCurrentIndex(self.current_index)

        self.item_added.emit(item)

    @property
    def current_item(self):
        return self.current_index.data()

    def refresh_current_index(self):
        self.list.dataChanged(self.current_index, self.current_index)

    def delete_current_item(self):
        if len(self.model) > 1:
            with block_signal([self.list]):
                row = self.current_index.row()

                item = self.current_item

                self.model.remove(self.current_index)

                if row == len(self.model):
                    row -= 1

                self.current_index = self.model.index(row)
                self.list.setCurrentIndex(self.current_index)

                self.item_deleted.emit(item)

    def handle_item_click(self, item):
        self.item_clicked.emit(self.current_index.data())

    def handle_item_change(self, selected, *args):
        if selected_index := selected.indexes():
            self.current_index = selected_index[0]

            self.item_changed.emit(self.current_index.data())
        else:
            self.list.setCurrentIndex(self.current_index)

    def get_items(self):
        return self.model.items

    def set_current_item(self, item):
        index = self.model.index(item.get_index_from(self.get_items()))

        self.list.setCurrentIndex(index)

    def next(self) -> Tuple[int, int]:
        current_row = self.current_index.row()
        next_row = current_row + 1

        if next_row >= len(self.model):
            next_row = 0

        self.current_index = self.model.index(next_row)
        self.list.setCurrentIndex(self.current_index)

        return current_row, next_row

    def previous(self) -> Tuple[int, int]:
        current_row = self.current_index.row()
        previous_row = current_row - 1

        if previous_row < 0:
            previous_row = len(self.model) - 1

        self.current_index = self.model.index(previous_row)
        self.list.setCurrentIndex(self.current_index)

        return current_row, previous_row

    def set_first_item_as_current_item(self) -> int:
        row = 0

        self.current_index = self.model.index(row)
        self.list.setCurrentIndex(self.current_index)

        return row

    def set_last_item_as_current_item(self) -> int:
        row = len(self.model) - 1

        self.current_index = self.model.index(row)
        self.list.setCurrentIndex(self.current_index)

        return row


class HarmonyGrid(BaseGrid):
    item_changed = Signal(HarmonyItem)
    item_clicked = Signal(HarmonyItem)

    delegate = HarmonyDelegate()

    def __init__(self, *args, harmony_items: List[HarmonyItem], **kwargs):
        super(HarmonyGrid, self).__init__(*args, **kwargs)

        self.setAttribute(Qt.WA_StyledBackground)

        self.add_button = IconButton(icon_path=Path("beethoven/ui/img/plus-32.png"))
        self.add_button.setObjectName("add_button")

        self.delete_button = IconButton(
            icon_path=Path("beethoven/ui/img/minus-7-32.png")
        )
        self.delete_button.setObjectName("delete_button")

        self.setup_list_view(ItemsModel(harmony_items))

        self.add_button.clicked.connect(self.add_item)
        self.delete_button.clicked.connect(self.delete_current_item)

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

    def get_default_item(self):
        return get_default_harmony_item()

    def update_item_scale(self, scale: Scale):
        self.current_item.scale = scale

        self.refresh_current_index()

    def update_item_bpm(self, bpm: Bpm):
        self.current_item.bpm = bpm

        self.refresh_current_index()

    def update_item_time_signature(self, time_signature: TimeSignature):
        self.current_item.time_signature = time_signature

        self.refresh_current_index()


class ChordGrid(BaseGrid):
    item_changed = Signal(ChordItem)
    item_clicked = Signal(ChordItem)

    delegate = ChordDelegate()

    def __init__(self, *args, chord_items: List[ChordItem], **kwargs):
        super(ChordGrid, self).__init__(*args, **kwargs)

        self.setAttribute(Qt.WA_StyledBackground)

        self.add_button = IconButton(icon_path=Path("beethoven/ui/img/plus-32.png"))
        self.modify_button = IconPushPullButton(
            icon_path=Path("beethoven/ui/img/gear-32.png")
        )
        self.delete_button = IconButton(
            icon_path=Path("beethoven/ui/img/minus-7-32.png")
        )

        self.setup_list_view(ItemsModel(chord_items))

        self.list.setObjectName("chord_list")

        self.add_button.clicked.connect(self.add_item)
        self.delete_button.clicked.connect(self.delete_current_item)

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

    def get_default_item(self):
        return get_default_chord_item()

    def set(self, chord_items: List[ChordItem], **kwargs):
        with block_signal([self.list]):
            self.model.set_items(chord_items)

            self.current_index = self.model.index(0)

            self.list.setCurrentIndex(self.current_index)

    def update_chord_item(self, chord_item: ChordItem):
        self.model.setData(self.current_index, chord_item)

        self.refresh_current_index()


class ComposerGrid(QWidget):
    harmony_item_changed = Signal(HarmonyItem, ChordItem)
    chord_item_changed = Signal(ChordItem)
    item_clicked = Signal(HarmonyItem, ChordItem)

    def __init__(self, *args, harmony_items: List[HarmonyItem], **kwargs):
        super(ComposerGrid, self).__init__(*args, **kwargs)

        self.harmony_items = harmony_items

        self.harmony_grid = HarmonyGrid(harmony_items=self.harmony_items)
        self.chord_grid = ChordGrid(chord_items=self.harmony_items[0].chord_items)

        self.harmony_grid.item_changed.connect(self.handle_harmony_item_change)
        self.harmony_grid.item_clicked.connect(self.handle_harmony_item_click)

        self.chord_grid.item_added.connect(self.harmony_grid.refresh_current_index)
        self.chord_grid.item_changed.connect(self.handle_chord_item_change)
        self.chord_grid.item_clicked.connect(self.handle_chord_item_click)
        self.chord_grid.item_deleted.connect(self.harmony_grid.refresh_current_index)

        self.setLayout(
            vertical_layout([self.harmony_grid, Spacing(size=4), self.chord_grid])
        )

    def next(self):
        _, chord_index = self.chord_grid.next()

        if not chord_index:
            self.harmony_grid.next()

    def previous(self):
        previous_chord_index, chord_index = self.chord_grid.previous()

        if chord_index > previous_chord_index:
            self.harmony_grid.previous()

            self.chord_grid.set_last_item_as_current_item()

    def get_current_items(self) -> Tuple[HarmonyItem, ChordItem]:
        return self.harmony_grid.current_item, self.chord_grid.current_item

    def handle_harmony_item_change(self, *args):
        self.refresh_chords_list()

    def handle_chord_item_change(self, chord_item: ChordItem):
        self.chord_item_changed.emit(chord_item)

    def handle_harmony_item_click(self, harmony_item):
        self.item_clicked.emit(harmony_item, harmony_item.chord_items[0])

    def handle_chord_item_click(self, chord_item):
        self.item_clicked.emit(self.harmony_grid.current_item, chord_item)

    def refresh_chords_list(self):
        harmony_item = self.harmony_grid.current_item

        self.chord_grid.set(harmony_item.chord_items, setup=True)

        self.harmony_item_changed.emit(*self.get_current_items())

    def update_chord_item(self, chord_item: ChordItem):
        self.chord_grid.update_chord_item(chord_item)

        self.harmony_grid.refresh_current_index()

    def set_current_items(self, harmony_item: HarmonyItem, chord_item: ChordItem):
        if self.harmony_grid.current_item.id != harmony_item.id:
            self.harmony_grid.set_current_item(harmony_item)

            if 0:
                self.refresh_chords_list()
            else:
                harmony_item = self.harmony_grid.current_item

                self.chord_grid.set(harmony_item.chord_items, setup=True)
        else:
            self.chord_grid.set_current_item(chord_item)
