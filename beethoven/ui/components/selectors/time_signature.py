import logging

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox, QLabel, QSpinBox, QWidget

from beethoven.models import TimeSignature
from beethoven.ui.layouts import Spacing, horizontal_layout
from beethoven.ui.utils import block_signal

logger = logging.getLogger("selectors.time_signature")


class TimeSignatureSelector(QWidget):
    value_changed = Signal(TimeSignature)

    def __init__(
        self,
        *args,
        time_signature=TimeSignature(beats_per_bar=4, beat_unit=4),
        **kwargs
    ):
        super(TimeSignatureSelector, self).__init__(*args, **kwargs)

        self.beats_per_bar_spinbox = QSpinBox()
        self.beats_per_bar_spinbox.setRange(1, 52)

        self.beat_unit_combobox = QComboBox()
        self.beat_unit_combobox.addItems("1,2,4,8,16,32".split(","))

        self.beats_per_bar_spinbox.valueChanged.connect(
            self.handle_beats_per_bar_change
        )
        self.beat_unit_combobox.currentTextChanged.connect(self.handle_beat_unit_change)

        self.set(time_signature)

        self.setLayout(
            horizontal_layout(
                [
                    self.beats_per_bar_spinbox,
                    Spacing(size=5),
                    QLabel("/"),
                    Spacing(size=5),
                    self.beat_unit_combobox,
                ]
            )
        )

    def set(self, time_signature: TimeSignature):
        self.value = time_signature

        with block_signal(
            [
                self.beats_per_bar_spinbox,
                self.beat_unit_combobox,
            ]
        ):
            self.beats_per_bar_spinbox.setValue(time_signature.beats_per_bar)
            self.beat_unit_combobox.setCurrentText(str(time_signature.beat_unit))

    def handle_beats_per_bar_change(self, value):
        if (
            value > self.beats_per_bar_spinbox.minimum()
            and value < self.beats_per_bar_spinbox.maximum()
        ):
            time_signature = TimeSignature(
                beats_per_bar=value,
                beat_unit=self.value.beat_unit,
            )

            self.value = time_signature

            self.value_changed.emit(self.value)

    def handle_beat_unit_change(self, value):
        time_signature = TimeSignature(
            beats_per_bar=self.value.beats_per_bar,
            beat_unit=int(value),
        )

        self.value = time_signature

        self.value_changed.emit(self.value)
