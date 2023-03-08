import logging

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox

from beethoven.settings import TuningSettings
from beethoven.ui.utils import block_signal

logger = logging.getLogger("combobox.tuning")


class TuningComboBox(QComboBox):
    value_changed = Signal(str)

    def __init__(self, *args, tuning_settings: TuningSettings, **kwargs):
        super(TuningComboBox, self).__init__(*args, **kwargs)

        self.tuning_settings = tuning_settings

        self.addItems(self.tuning_settings.tunings.keys())

        self.set(list(self.tuning_settings.defaults.keys())[0])

        self.currentTextChanged.connect(self.handle_tuning_change)

    def add(self, tuning_name):
        if self.findText(tuning_name) == -1:
            self.addItem(tuning_name)

    def set(self, tuning_name: str):
        self.value = tuning_name

        with block_signal([self]):
            self.setCurrentText(tuning_name)

    def refresh(self):
        self.clear()

        tuning_names = list(self.tuning_settings.tunings.keys())

        self.addItems(tuning_names)

        if self.value in tuning_names:
            self.set(self.value)
        else:
            self.setCurrentText(tuning_names[0])

            self.value = tuning_names[0]

    def delete_current(self):
        current_index = self.currentIndex()

        self.setCurrentIndex(current_index - 1)
        self.removeItem(current_index)

    def handle_tuning_change(self, tuning_name):
        logger.debug(f"change to {tuning_name}")

        self.value = tuning_name

        self.value_changed.emit(tuning_name)
