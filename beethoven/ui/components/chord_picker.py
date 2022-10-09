from logging import getLogger
from typing import Union

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from beethoven.models import Degree, Note, Scale
from beethoven.ui.components.selectors import (
    ChordGridSelector,
    DegreeGridSelector,
    RootGridSelector,
)
from beethoven.ui.layouts import vertical_layout
from beethoven.ui.managers import AppManager
from beethoven.ui.models import ChordItem

logger = getLogger("chord_picker")


class ChordPicker(QWidget):
    chord_item_changed = Signal(ChordItem)

    def __init__(
        self,
        *args,
        manager: AppManager,
        current_chord_item: ChordItem,
        current_scale: Scale,
        **kwargs
    ):
        super(ChordPicker, self).__init__(*args, **kwargs)

        self.manager = manager

        self.current_scale = current_scale

        self.root_grid_selector = RootGridSelector(grid_width=12)
        self.degree_grid_selector = DegreeGridSelector(grid_width=12)
        self.chord_grid_selector = ChordGridSelector(grid_width=7)

        self.set_chord_item(current_chord_item)

        self.root_grid_selector.root_changed.connect(self.update_root)
        self.degree_grid_selector.degree_changed.connect(self.update_root)
        self.chord_grid_selector.chord_name_changed.connect(self.update_chord_name)

        self.setLayout(
            vertical_layout([
                self.chord_grid_selector,
                self.root_grid_selector,
                self.degree_grid_selector,
            ])
        )

    def set_chord_item(self, chord_item: ChordItem):
        self.current_chord_name = chord_item.name
        self.current_chord_root = chord_item.root

        self.root_grid_selector.clear()
        self.degree_grid_selector.clear()

        if isinstance(chord_item.root, Note):
            self.root_grid_selector.set_root(chord_item.root)
        elif isinstance(chord_item.root, Degree):
            self.degree_grid_selector.set_degree(chord_item.root)

        self.chord_grid_selector.set_chord_name(chord_item.name)

    def set_scale(self, scale: Scale):
        self.current_scale = scale

    def update_root(self, root: Union[Note, Degree]):
        logger.debug(f"updated chord root to {str(root)}")

        if isinstance(root, Note):
            self.degree_grid_selector.clear()

        elif isinstance(root, Degree):
            self.root_grid_selector.clear()

        self.current_chord_root = root

        self.update_chord_item()

    def update_chord_name(self, chord_name):
        logger.debug(f"updated chord name to {chord_name or 'none'}")

        self.current_chord_name = chord_name

        self.update_chord_item()

    def update_chord_item(self):
        self.chord_item_changed.emit(
            ChordItem(
                name=self.current_chord_name,
                root=self.current_chord_root,
            )
        )
