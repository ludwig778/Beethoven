import logging

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox

from beethoven import indexes
from beethoven.ui.utils import block_signal

logger = logging.getLogger("combobox.scale")


class ScaleComboBox(QComboBox):
    value_changed = Signal(str)

    def __init__(self, *args, scale_name: str, **kwargs):
        super(ScaleComboBox, self).__init__(*args, **kwargs)

        self.scale_names = self._get_scale_names()

        self.addItems(self.scale_names)

        self.set(scale_name)

        self.currentTextChanged.connect(self.handle_scale_change)

    def set(self, scale_name: str):
        self.value = scale_name

        with block_signal([self]):
            self.setCurrentIndex(self.scale_names.index(scale_name))

    def handle_scale_change(self, scale_name):
        logger.debug(f"change to {scale_name}")

        self.value = scale_name

        self.value_changed.emit(self.value)

    def _get_scale_names(self):
        return [
            scale_data.names[0]
            for scale_data in indexes.scale_index.get_scales_by_label_data(["main_diatonic", "major"])
        ]
