from PySide6.QtWidgets import QAbstractItemView, QListWidget

from beethoven.ui.utils import set_object_name


class MidiOutputSelector(QListWidget):
    def __init__(self, *args, **kwargs):
        super(MidiOutputSelector, self).__init__(*args, **kwargs)

        set_object_name(self, **kwargs)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    @property
    def current_output_names(self):
        return [item.text() for item in self.selectedItems()]

    def list_outputs(self):
        return [item.text for item in self.selectedItems()]

    def add_output(self, output_name: str):
        if output_name not in self.list_outputs():
            self.addItem(output_name)

    def delete_output(self, output_name):
        for item in self.selectedItems():
            if output_name == item.text():
                self.takeItem(self.row(item))
