import logging

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QWidget

from beethoven.models import Bpm, HarmonyItem
from beethoven.ui.components.scale_picker import ScalePicker
from beethoven.ui.components.selectors.time_signature import TimeSignatureSelector
from beethoven.ui.components.spinbox import BpmSpinBox
from beethoven.ui.constants import C_MAJOR4
from beethoven.ui.layouts import Stretch, horizontal_layout, vertical_layout

logger = logging.getLogger("harmony_picker")


class HarmonyPicker(QWidget):
    value_changed = Signal(object, object, object)

    def __init__(self, *args, **kwargs):
        super(HarmonyPicker, self).__init__(*args, **kwargs)

        self.scale_picker = ScalePicker(scale=C_MAJOR4)
        self.time_signature_selector = TimeSignatureSelector()
        self.bpm_spinbox = BpmSpinBox()

        self.scale_picker.value_changed.connect(self.handle_scale_change)
        self.time_signature_selector.value_changed.connect(self.handle_time_signature_change)
        self.bpm_spinbox.value_changed.connect(self.handle_bpm_change)

        self.setLayout(
            horizontal_layout(
                [
                    vertical_layout(
                        [
                            QLabel("Scale :"),
                            QLabel("Time Signature :"),
                            QLabel("Bpm :"),
                        ],
                        object_name="label_section",
                    ),
                    vertical_layout(
                        [
                            self.scale_picker,
                            horizontal_layout([self.time_signature_selector, Stretch()]),
                            horizontal_layout([self.bpm_spinbox, Stretch()]),
                        ]
                    ),
                ]
            ),
        )

    @property
    def scale(self):
        return self.scale_picker.value

    @property
    def time_signature(self):
        return self.time_signature_selector.value

    @property
    def bpm(self):
        return self.bpm_spinbox.value()

    def set(self, harmony_item: HarmonyItem):
        self.scale_picker.set(harmony_item.scale)
        self.time_signature_selector.set(harmony_item.time_signature)
        self.bpm_spinbox.set(harmony_item.bpm)

    def handle_scale_change(self, scale):
        logger.debug(scale.to_log_string())

        self.value_changed.emit(scale, None, None)

    def handle_time_signature_change(self, time_signature):
        logger.debug(str(time_signature))

        self.value_changed.emit(None, time_signature, None)

    def handle_bpm_change(self, bpm: Bpm):
        logger.debug(str(bpm))

        self.value_changed.emit(None, None, bpm)
