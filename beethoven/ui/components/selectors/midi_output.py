from typing import List

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QAbstractItemView, QListWidget

from beethoven.ui.managers.app import AppManager
from beethoven.ui.utils import block_signal


class MidiOutputSelector(QListWidget):
    values_changed = Signal(list)

    def __init__(self, *args, manager: AppManager, **kwargs):
        super(MidiOutputSelector, self).__init__(*args, **kwargs)

        self.manager = manager

        self.refresh()

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    @property
    def values(self) -> List[str]:
        return list(sorted([item.text() for item in self.selectedItems()]))

    def add(self, output_name: str):
        if output_name not in self.manager.settings.midi.opened_outputs:
            self.addItem(output_name)

            self.manager.adapters.midi.open_output(output_name)

            self.manager.settings.midi.opened_outputs.append(output_name)
            self.manager.configuration_changed.emit()

    def delete_selected_outputs(self):
        for output_item in self.selectedItems():
            output_name = output_item.text()

            self.takeItem(self.row(output_item))

            self.manager.adapters.midi.close_output(output_name)
            self.manager.settings.midi.opened_outputs.remove(output_name)

        self.manager.configuration_changed.emit()

    def refresh(self):
        with block_signal([self]):
            self.clear()

            for output_name in self.manager.settings.midi.opened_outputs:
                self.addItem(output_name)
