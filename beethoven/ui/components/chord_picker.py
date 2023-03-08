import logging
from typing import List, Optional, Union

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QWidget

from beethoven.models import ChordItem, Degree, DurationItem, Interval, Note
from beethoven.ui.components.combobox.degree_alteration import DegreeAlterationComboBox
from beethoven.ui.components.selectors import ChordGridSelector, DegreeGridSelector, RootGridSelector
from beethoven.ui.components.selectors.duration import DurationSelector
from beethoven.ui.components.selectors.grid.base_note import BaseNoteGridSelector
from beethoven.ui.components.selectors.grid.extensions import ExtensionsGridSelector
from beethoven.ui.components.spinbox import InversionSpinBox
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

        self.value = chord_item

        note = None
        degree = None

        if isinstance(chord_item.root, Note):
            note = chord_item.root
        else:
            degree = chord_item.root

        self.chord_grid_selector = ChordGridSelector(chord_name=chord_item.name)
        self.root_grid_selector = RootGridSelector(root=note)
        self.degree_grid_selector = DegreeGridSelector(degree=degree)
        self.degree_alteration_combobox = DegreeAlterationComboBox(
            alteration=degree.alteration if degree else 0
        )
        self.duration_selector = DurationSelector(duration_item=chord_item.duration_item)
        self.inversion_spinbox = InversionSpinBox(chord_item=chord_item)
        self.base_note_grid_selector = BaseNoteGridSelector(base_note=chord_item.base_note)
        self.extensions_grid_selector = ExtensionsGridSelector(extensions=chord_item.extensions)

        self.chord_grid_selector.value_changed.connect(self.handle_chord_name_change)
        self.root_grid_selector.value_changed.connect(self.handle_root_change)
        self.degree_grid_selector.value_changed.connect(self.handle_root_change)
        self.degree_alteration_combobox.value_changed.connect(self.handle_degree_alteration_change)
        self.duration_selector.value_changed.connect(self.handle_chord_duration_item_change)
        self.inversion_spinbox.value_changed.connect(self.handle_inversion_change)
        self.base_note_grid_selector.value_changed.connect(self.handle_base_note_change)
        self.extensions_grid_selector.value_changed.connect(self.handle_extensions_change)

        degree_selector_layout = horizontal_layout(
            [
                self.degree_grid_selector,
                self.degree_alteration_combobox,
            ]
        )

        layout_items = [
            QLabel("Chord name:"),
            Spacing(size=5),
            self.chord_grid_selector,
            Spacing(size=10),
            QLabel("Root:"),
            Spacing(size=5),
            degree_selector_layout,
            Spacing(size=10),
            QLabel("Base Note:"),
            Spacing(size=5),
            self.base_note_grid_selector,
            QLabel("Extensions:"),
            Spacing(size=5),
            self.extensions_grid_selector,
            Spacing(size=18),
            horizontal_layout(
                [
                    Stretch(),
                    QLabel("Duration:"),
                    self.duration_selector,
                    Spacing(size=30),
                    QLabel("Inversion:"),
                    self.inversion_spinbox,
                    Stretch(),
                ],
                object_name="duration_section",
            ),
            Spacing(size=16),
        ]

        if show_root_notes:
            layout_items.insert(6, self.root_grid_selector)

        self.setLayout(vertical_layout(layout_items))  # type: ignore

    def set(self, chord_item: ChordItem):
        self.value = chord_item

        with block_signal(
            [
                self.chord_grid_selector,
                self.root_grid_selector,
                self.degree_grid_selector,
                self.degree_alteration_combobox,
                self.inversion_spinbox,
                self.base_note_grid_selector,
                self.extensions_grid_selector,
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
            self.inversion_spinbox.set(chord_item)
            self.duration_selector.set(self.value.duration_item)
            self.base_note_grid_selector.set(chord_item.base_note)
            self.extensions_grid_selector.set(chord_item.extensions)

            if self.inversion_spinbox.value() != chord_item.inversion:
                self.value.inversion = self.inversion_spinbox.value()

                self.value_changed.emit(self.value)

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

        self.value.root = Degree(name=self.value.root.name, alteration=degree_alteration)

        self.value_changed.emit(self.value)

    def handle_chord_name_change(self, chord_name: str):
        logger.debug(f"{chord_name or 'none'}")

        self.value.name = chord_name

        with block_signal([self.inversion_spinbox]):
            self.inversion_spinbox.set(self.value)

            inversion = self.inversion_spinbox.value()

            if self.value.inversion != inversion:
                self.value.inversion = inversion

        self.value_changed.emit(self.value)

    def handle_chord_duration_item_change(self, duration_item: DurationItem):
        self.value.duration_item = duration_item

        self.value_changed.emit(self.value)

    def handle_inversion_change(self, inversion: int):
        logger.debug(str(inversion))

        self.value.inversion = inversion

        self.value_changed.emit(self.value)

    def handle_base_note_change(self, base_note: Optional[Note] = None):
        logger.debug(str(base_note))

        self.value.base_note = base_note

        self.value_changed.emit(self.value)

    def handle_extensions_change(self, extensions: Optional[List[Interval]] = None):
        logger.debug(",".join([str(e) for e in extensions]) if extensions else None)

        self.value.extensions = extensions

        self.value_changed.emit(self.value)
