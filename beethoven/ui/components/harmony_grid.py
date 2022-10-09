from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from beethoven.models.scale import Scale
from beethoven.ui.components.buttons import Button
from beethoven.ui.components.list import ChordListWidget, HarmonyListWidget
from beethoven.ui.dialogs.chord_picker import ChordPickerDialog
from beethoven.ui.layouts import horizontal_layout, vertical_layout
from beethoven.ui.managers import AppManager
from beethoven.ui.models import ChordItem, HarmonyItem, HarmonyItems
from beethoven.ui.sizing import VerticalExplandPolicy, set_size_policies
from beethoven.ui.utils import block_signal, get_default_chord_item, get_default_harmony_item, run_method_on_widgets


class HarmonyGrid(QWidget):
    harmony_item_changed = Signal(HarmonyItem, ChordItem)
    chord_item_changed = Signal(ChordItem)

    def __init__(
        self, *args, manager: AppManager, harmony_items: HarmonyItems, **kwargs
    ):
        super(HarmonyGrid, self).__init__(*args, **kwargs)

        self.manager = manager
        self.harmony_items = harmony_items

        self.add_harmony_button = Button("Add")
        self.delete_harmony_button = Button("Delete")
        self.add_chord_button = Button("Add")
        self.delete_chord_button = Button("Delete")

        self.harmony_list = HarmonyListWidget(harmony_items=harmony_items)
        self.chord_list = ChordListWidget(harmony_item=harmony_items.items[0])

        self.add_harmony_button.clicked.connect(self.add_harmony_item)
        self.delete_harmony_button.clicked.connect(self.delete_current_harmony_item)

        self.add_chord_button.clicked.connect(self.add_chord_item)
        self.delete_chord_button.clicked.connect(self.delete_current_chord_item)

        self.harmony_list.currentItemChanged.connect(self.update_chords_list)
        self.chord_list.currentItemChanged.connect(self.update_chord)
        self.chord_list.itemDoubleClicked.connect(self.update_current_chord)

        self.setFixedHeight(160)
        self.setMinimumWidth(350)

        self.harmony_list.setFixedHeight(90)
        self.chord_list.setFixedHeight(55)

        run_method_on_widgets(
            QWidget.setFixedWidth,
            [
                self.add_harmony_button,
                self.delete_harmony_button,
                self.add_chord_button,
                self.delete_chord_button,
            ],
            70,
        )

        set_size_policies(
            [
                self.harmony_list,
                self.chord_list,
                self.add_harmony_button,
                self.delete_harmony_button,
                self.add_chord_button,
                self.delete_chord_button,
            ],
            VerticalExplandPolicy,
        )

        self.setLayout(
            vertical_layout([
                horizontal_layout([
                    self.harmony_list,
                    vertical_layout([
                        self.add_harmony_button,
                        self.delete_harmony_button,
                    ]),
                ]),
                horizontal_layout([
                    self.chord_list,
                    vertical_layout([
                        self.add_chord_button,
                        self.delete_chord_button,
                    ]),
                ]),
            ])
        )

    def next(self):
        chord_len = self.chord_list.count()
        next_chord_row = self.chord_list.currentRow() + 1

        if next_chord_row < chord_len:
            self.chord_list.setCurrentRow(next_chord_row)

        else:
            harmony_len = self.harmony_list.count()
            next_harmony_row = self.harmony_list.currentRow() + 1

            if next_harmony_row < harmony_len:
                self.harmony_list.setCurrentRow(next_harmony_row)
            else:
                self.chord_list.setCurrentRow(0)
                self.harmony_list.setCurrentRow(0)

    def get_current_item(self):
        return (
            self.harmony_list.get_current_harmony_item(),
            self.chord_list.get_current_chord_item(),
        )

    def add_harmony_item(self):
        self.harmony_list.add_item(get_default_harmony_item())

    def delete_current_harmony_item(self):
        with block_signal([self.harmony_list]):
            self.harmony_list.delete_current_item()

            self.update_chords_list()

    def update_chord(self):
        self.chord_item_changed.emit(self.chord_list.get_current_chord_item())

    def update_chords_list(self):
        harmony_item = self.harmony_items.items[self.harmony_list.currentRow()]

        with block_signal([self.chord_list]):
            self.chord_list.set_chords(harmony_item, setup=True)

        self.harmony_item_changed.emit(
            self.harmony_list.get_current_harmony_item(),
            self.chord_list.get_current_chord_item(),
        )

    def add_chord_item(self):
        self.chord_list.add_item(get_default_chord_item())

        self.harmony_list.update_current_item()

    def delete_current_chord_item(self):
        with block_signal([self.harmony_list, self.chord_list]):
            self.chord_list.delete_current_item()

            self.harmony_list.update_current_item()

        self.update_chord()

    def update_current_chord2(self):
        harmony_item = self.harmony_items.items[self.harmony_list.currentRow()]
        chord_item = harmony_item.chord_items[self.chord_list.currentRow()]

        picker = ChordPickerDialog(
            manager=self.manager,
            current_chord_item=chord_item,
            current_scale=harmony_item.scale,
        )

        ok, chord_item = picker.get_new_chord()

        if not ok:
            return

    def update_current_chord(self, chord_item: ChordItem):
        self.chord_list.update_current_item(chord_item)
        self.harmony_list.update_current_item()

    def update_current_scale(self, scale: Scale):
        harmony_item = self.harmony_list.get_current_harmony_item()
        harmony_item.scale = scale

        self.harmony_list.update_current_item()
