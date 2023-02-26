import logging

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox

from beethoven.ui.utils import block_signal

logger = logging.getLogger("combobox.degree_alteration")


class DegreeAlterationComboBox(QComboBox):
    value_changed = Signal(int)
    available_alterations = "♯♯,♯,♮,♭,♭♭".split(",")

    def __init__(self, *args, alteration: int = 0, **kwargs):
        super(DegreeAlterationComboBox, self).__init__(*args, **kwargs)

        self.addItems(self.available_alterations)

        self.set(alteration)

        self.currentTextChanged.connect(self.handle_alteration_change)

    def set(self, alteration: int):
        self.value = alteration

        with block_signal([self]):
            self.setCurrentIndex(2 - alteration)

    def handle_alteration_change(self, alteration_string):
        alteration = self._get_alteration_from_str(alteration_string)

        self.value = alteration

        self.value_changed.emit(self.value)

    def reset(self):
        self.set(0)

    def _get_alteration_from_str(self, alteration_string: str):
        return 2 - self.available_alterations.index(alteration_string)
