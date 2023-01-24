from logging import getLogger
from typing import Sequence

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QWidget

from beethoven.models import Note
from beethoven.ui.components.combobox import NoteComboBox
from beethoven.ui.layouts import Stretch, horizontal_layout, vertical_layout
from beethoven.ui.settings import TuningSetting

logger = getLogger("selectors.string")


class StringSelectorRow(QWidget):
    value_changed = Signal(Note)

    def __init__(self, *args, note: Note, **kwargs):
        super(StringSelectorRow, self).__init__(*args, **kwargs)

        self.number_label = QLabel()
        self.note_combobox = NoteComboBox(note=note)

        self.set(note)

        self.note_combobox.value_changed.emit(self.value_changed)

        self.setLayout(horizontal_layout([self.number_label, self.note_combobox]))

    @property
    def value(self):
        return self.note_combobox.value

    def set_label(self, text: str) -> None:
        self.number_label.setText(text)

    def set(self, note: Note):
        self.note_combobox.set(note)


class StringSelector(QWidget):
    value_changed = Signal(TuningSetting)
    DEFAULT_NOTE = Note.parse("A")
    STRING_ORDER = [2, 3, 4, 5, 1, 0, 6, 7]

    def __init__(self, *args, initial_tuning=None, **kwargs):
        super(StringSelector, self).__init__(*args, **kwargs)

        self.string_rows: Sequence = [StringSelectorRow(note=self.DEFAULT_NOTE) for _ in range(8)]
        layout_items = self.string_rows + [Stretch()]

        self.set(initial_tuning)

        for string_row in self.string_rows:
            string_row.value_changed.emit(self.handle_tuning_change)

        self.setLayout(vertical_layout(layout_items))

    def set(self, tuning: TuningSetting):
        self.value = tuning

        self.update_string_rows(self.value)

    def update_string_rows(self, tuning: TuningSetting):
        string_number = len(tuning.notes)

        offset = 0
        if string_number in (4, 5):
            offset = 6 - string_number

        for index, note in enumerate(reversed(tuning.notes)):
            self.string_rows[index + offset].set(note)

        self.update_string_number(string_number)

    def update_string_number(self, string_number: int):
        displayed_rows = []

        for index, string_order_row in enumerate(self.STRING_ORDER):
            string_row = self.string_rows[string_order_row]

            if string_number > index:
                string_row.setVisible(True)
                displayed_rows.append(string_row)
            else:
                string_row.setVisible(False)

        string_index = 1
        for string_row in self.string_rows:
            if string_row in displayed_rows:
                string_row.set_label(f"String {string_index}")

                string_index += 1

    def handle_tuning_change(self):
        tuning = TuningSetting(
            notes=[
                string_row.value
                for string_row in reversed(self.string_rows)
                if string_row.isVisible()
            ]
        )

        self.value = tuning

        self.value_changed.emit(self.value)
