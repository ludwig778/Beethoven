import logging
from typing import Union

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QWidget

from beethoven.models import ChordItem, Degree, DurationItem, Note
from beethoven.ui.components.combobox.degree_alteration import DegreeAlterationComboBox
from beethoven.ui.components.selectors import (
    ChordGridSelector,
    DegreeGridSelector,
    RootGridSelector,
)
from beethoven.ui.components.selectors.duration import DurationSelector
from beethoven.ui.layouts import Spacing, Stretch, horizontal_layout, vertical_layout
from beethoven.ui.utils import block_signal

logger = logging.getLogger("chord_picker")


class ChordPicker(QWidget):
    value_changed = Signal(ChordItem)

    def __init__(
        self,
        *args,
        chord_item: ChordItem,
        show_root_notes: bool = True,
        **kwargs,
    ):
        super(ChordPicker, self).__init__(*args, **kwargs)

        self.root_grid_selector = RootGridSelector(grid_width=12)
        self.degree_grid_selector = DegreeGridSelector(grid_width=12)
        self.chord_grid_selector = ChordGridSelector(grid_width=7)

        self.duration_selector = DurationSelector(
            duration_item=chord_item.duration_item
        )

        self.degree_alteration_combobox = DegreeAlterationComboBox()

        self.set(chord_item)

        self.root_grid_selector.value_changed.connect(self.handle_root_change)
        self.degree_grid_selector.value_changed.connect(self.handle_root_change)
        self.chord_grid_selector.value_changed.connect(self.handle_chord_name_change)
        self.duration_selector.value_changed.connect(
            self.handle_chord_duration_item_change
        )

        self.degree_alteration_combobox.value_changed.connect(
            self.handle_degree_alteration_change
        )

        degree_selector_layout = horizontal_layout(
            [
                self.degree_grid_selector,
                self.degree_alteration_combobox,
            ]
        )

        layout_items = [
            QLabel("Chord name:"),
            self.chord_grid_selector,
            Spacing(size=10),
            QLabel("Root:"),
            degree_selector_layout,
            Spacing(size=20),
            horizontal_layout(
                [
                    QLabel("Duration:"),
                    self.duration_selector,
                    Stretch(),
                ],
                object_name="duration_section",
            ),
            Spacing(size=15),
        ]
        if show_root_notes:
            layout_items.insert(4, self.root_grid_selector)

        self.setLayout(vertical_layout(layout_items))  # type: ignore

    def set(self, chord_item: ChordItem):
        self.value = chord_item

        with block_signal(
            [
                self.root_grid_selector,
                self.degree_grid_selector,
                self.degree_alteration_combobox,
            ]
        ):
            self.root_grid_selector.clear()
            self.degree_grid_selector.clear()

            if isinstance(self.value.root, Note):
                self.root_grid_selector.set(self.value.root)
                self.degree_alteration_combobox.reset()
            elif isinstance(chord_item.root, Degree):
                self.degree_grid_selector.set(self.value.root)
                self.degree_alteration_combobox.set(self.value.root.alteration)

                self.chord_grid_selector.set(self.value.name)

                self.duration_selector.set(self.value.duration_item)

    def handle_root_change(self, root: Union[Note, Degree]):
        logger.debug(f"updated chord root to {str(root)}")

        if isinstance(root, Note):
            self.degree_grid_selector.clear()

            self.value.root = root

        elif isinstance(root, Degree):
            self.root_grid_selector.clear()

            if self.degree_alteration_combobox.value:
                self.value.root = Degree(
                    name=root.name, alteration=self.degree_alteration_combobox.value
                )
            else:
                self.value.root = root

        self.value_changed.emit(self.value)

    def handle_degree_alteration_change(self, alteration: int):
        if not isinstance(self.value.root, Degree):
            return

        logger.debug(f"updated chord root degree alteration to {alteration}")

        degree_alteration = self.degree_alteration_combobox.value

        self.value.root = Degree(
            name=self.value.root.name, alteration=degree_alteration
        )

        self.value_changed.emit(self.value)

    def handle_chord_name_change(self, chord_name: str):
        logger.debug(f"updated chord name to {chord_name or 'none'}")

        self.value.name = chord_name

        self.value_changed.emit(self.value)

    def handle_chord_duration_item_change(self, duration_item: DurationItem):
        self.value.duration_item = duration_item

        self.value_changed.emit(self.value)
