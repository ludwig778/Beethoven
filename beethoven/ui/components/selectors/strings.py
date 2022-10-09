from logging import getLogger

from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

import beethoven.controllers.note as note_controller
from beethoven.ui.components.combobox import NoteComboBox
from beethoven.ui.settings import TuningSetting

logger = getLogger("selectors.string")


class StringSelectorRow(QWidget):
    def __init__(self, *args, note=None, **kwargs):
        super(StringSelectorRow, self).__init__(*args, **kwargs)

        self.label = QLabel()
        self.note_combobox = NoteComboBox(selected_note=note)

        self.setLayout(self.get_layout())

    def set_label(self, text: str) -> None:
        self.label.setText(text)

    def set_note(self, note):
        return self.note_combobox.set_note(note)

    def get_note(self):
        return self.note_combobox.get_note()

    def get_layout(self):
        main_layout = QHBoxLayout()

        main_layout.addWidget(self.label)
        main_layout.addWidget(self.note_combobox)

        return main_layout


class StringSelector(QWidget):
    DEFAULT_NOTE = note_controller.parse("A")
    STRING_ORDER = [2, 3, 4, 5, 1, 0, 6, 7]

    def __init__(self, *args, initial_tuning=None, **kwargs):
        super(StringSelector, self).__init__(*args, **kwargs)

        self.setup()

        self.set_tuning(initial_tuning)

        self.update_string_widgets(len(initial_tuning.notes))

    def setup(self):
        logger.debug("setup")

        self.string_row_widgets = [
            StringSelectorRow(note=self.DEFAULT_NOTE) for _ in range(8)
        ]

        self.setLayout(self.get_layout())

    def get_layout(self):
        main_layout = QVBoxLayout()

        for string_row_widget in self.string_row_widgets:
            main_layout.addWidget(string_row_widget)

        main_layout.addStretch()

        return main_layout

    def update_string_widgets(self, string_number: int):
        displayed_rows = []
        for index, string_order_row in enumerate(self.STRING_ORDER):
            row_widget = self.string_row_widgets[string_order_row]

            if string_number > index:
                row_widget.setVisible(True)
                displayed_rows.append(row_widget)
            else:
                row_widget.setVisible(False)

        string_index = 1
        for row_widget in self.string_row_widgets:
            if row_widget in displayed_rows:
                row_widget.set_label(f"String {string_index}")

                string_index += 1

    def set_tuning(self, tuning: TuningSetting):
        note_count = len(tuning.notes)

        offset = 0
        if note_count in (4, 5):
            offset = 6 - note_count

        for i, a in enumerate(reversed(tuning.notes)):
            self.string_row_widgets[i + offset].set_note(a)

    def get_tuning(self):
        return TuningSetting(
            notes=[
                string_row.get_note()
                for string_row in reversed(self.string_row_widgets)
                if string_row.isVisible()
            ]
        )
