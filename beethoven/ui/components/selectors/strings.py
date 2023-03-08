import logging
from typing import List, Tuple, cast

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QWidget

from beethoven.models import Note
from beethoven.settings import TuningSetting
from beethoven.ui.components.combobox import NoteComboBox
from beethoven.ui.layouts import LayoutItems, Stretch, horizontal_layout, vertical_layout

logger = logging.getLogger("selectors.string")


class StringSelector(QWidget):
    value_changed = Signal(TuningSetting)
    DEFAULT_NOTE = Note.parse("A")
    STRING_ORDER = [2, 3, 4, 5, 1, 0, 6, 7]

    def __init__(self, *args, initial_tuning=None, **kwargs):
        super(StringSelector, self).__init__(*args, **kwargs)

        layout_items: LayoutItems = []

        self.string_rows: List[Tuple[QLabel, NoteComboBox]] = []
        self.string_row_widgets: List[QWidget] = []

        for _ in range(8):
            note_combobox = NoteComboBox(note=self.DEFAULT_NOTE)
            note_combobox.value_changed.connect(self.handle_tuning_change)

            string_row = (QLabel(""), note_combobox)

            widget = QWidget()
            widget.setLayout(horizontal_layout(cast(LayoutItems, string_row)))
            widget.setObjectName("string_selector_row")

            self.string_rows.append(string_row)
            self.string_row_widgets.append(widget)

            layout_items.append(widget)

        self.set(initial_tuning)

        layout_items.append(Stretch())

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
            self.string_rows[index + offset][1].set(note)

        self.update_string_number(string_number)

    def update_string_number(self, string_number: int):
        displayed_string_rows = []

        for index, string_order_row in enumerate(self.STRING_ORDER):
            string_row = self.string_rows[string_order_row]
            string_row_widget = self.string_row_widgets[string_order_row]

            if string_number > index:
                string_row_widget.setVisible(True)
                displayed_string_rows.append(string_row)
            else:
                string_row_widget.setVisible(False)

        string_index = 1
        for string_row in self.string_rows:
            if string_row not in displayed_string_rows:
                continue

            string_row[0].setText(f"String {string_index}")

            string_index += 1

        self.handle_tuning_change()

    def handle_tuning_change(self):
        tuning_notes = []

        for string_row, string_row_widget in zip(self.string_rows[::-1], self.string_row_widgets[::-1]):
            if string_row_widget.isVisible():
                tuning_notes.append(string_row[1].value)

        tuning = TuningSetting(notes=tuning_notes)

        self.value = tuning

        self.value_changed.emit(self.value)
