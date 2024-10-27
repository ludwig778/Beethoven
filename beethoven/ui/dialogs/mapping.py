import logging
from functools import partial

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QLabel

from beethoven.sequencer.objects import Mapping
from beethoven.ui.components.combobox.note import NoteWithOctaveComboBox
from beethoven.ui.layouts import (Stretch, clear_layout, horizontal_layout,
                                  vertical_layout)
from beethoven.ui.managers import AppManager

logger = logging.getLogger("dialog.mapping")


class MappingDialog(QDialog):
    configuration_changed = Signal()

    def __init__(self, *args, manager: AppManager, **kwargs):
        super(MappingDialog, self).__init__(*args, **kwargs)

        self.manager = manager
        self.mapping: Mapping | None = None

        # self.setStyleSheet("min-width: 100px;")#min-height: 300px;")

        # self.layout = vertical_layout([Stretch()], margins=(10, 10, 10, 10))
        self.main_layout = vertical_layout([])

        self.setLayout(vertical_layout([self.main_layout, Stretch()], margins=(10, 10, 10, 10)))

    def clear(self):
        clear_layout(self.main_layout)

    def set_mapping(self, mapping: Mapping):
        self.mapping = mapping

        self.clear()

        for k, v in mapping.mappings.items():
            note_combobox = NoteWithOctaveComboBox(note=v)
            note_combobox.value_changed.connect(partial(self.handle_note_change, k))
            self.main_layout.addLayout(
                horizontal_layout(
                    [
                        QLabel(k),
                        Stretch(),
                        note_combobox,
                    ]
                )
            )

    def handle_note_change(self, key, value):
        print(key, value)
        if not self.mapping:
            return

        self.mapping.mappings[key] = value or None

        from pprint import pprint

        pprint(self.mapping)
