from logging import getLogger

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox

from beethoven import indexes
from beethoven.ui.utils import set_object_name

logger = getLogger("combobox.scale")


class ScaleComboBox(QComboBox):
    scale_name_changed = Signal(str)

    def __init__(self, *args, selected_scale_name: str, **kwargs):
        super(ScaleComboBox, self).__init__(*args, **kwargs)

        set_object_name(self, **kwargs)

        self.scale_names = [
            scale_data.names[0]
            for scale_data in indexes.scale_index.get_scales_by_label_data(
                ["main_diatonic", "major"]
            )
        ]

        for scale_name in self.scale_names:
            self.addItem(scale_name)

        self.set_scale_name(selected_scale_name)

        self.currentTextChanged.connect(self.on_scale_change)

    def set_scale_name(self, scale_name: str):
        self.setCurrentIndex(self.scale_names.index(scale_name))

    def get_scale_name(self) -> str:
        return self.scale_names[self.currentIndex()]

    def on_scale_change(self, scale_name):
        logger.debug(f"change to {scale_name}")

        self.scale_name_changed.emit(scale_name)
