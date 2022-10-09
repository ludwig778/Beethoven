from logging import getLogger

from PySide6.QtWidgets import QComboBox

from beethoven.ui.settings import TuningSettings
from beethoven.ui.utils import set_object_name

logger = getLogger("combobox.tuning")


class TuningComboBox(QComboBox):
    def __init__(self, *args, tuning_settings: TuningSettings, **kwargs):
        super(TuningComboBox, self).__init__(*args, **kwargs)

        set_object_name(self, **kwargs)

        self.tuning_settings = tuning_settings

        for tuning_name in self.tuning_settings.tunings.keys():
            self.addItem(tuning_name)

        self.setCurrentIndex(0)

        self.currentTextChanged.connect(self.on_tuning_change)

    @property
    def current_tuning_name(self):
        return self.currentText()

    @property
    def current_tuning(self):
        return self.tuning_settings.tunings.get(self.currentText())

    def add_tuning(self, tuning_name):
        if self.findText(tuning_name) == -1:
            self.addItem(tuning_name)

    def set_tuning(self, tuning_name):
        self.setCurrentText(tuning_name)

    def delete_current_tuning(self):
        current_index = self.currentIndex()

        self.setCurrentIndex(current_index - 1)
        self.removeItem(current_index)

    def on_tuning_change(self, tuning_name):
        logger.debug(f"change to {tuning_name}")
