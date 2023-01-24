from PySide6.QtCore import Signal
from PySide6.QtWidgets import QSpinBox

from beethoven.models import Bpm
from beethoven.ui.utils import block_signal


class SpinBox(QSpinBox):
    def __init__(self, *args, minimum: int, maximum: int, **kwargs):
        super(SpinBox, self).__init__(*args, **kwargs)

        self.setRange(minimum, maximum)

    @property
    def value(self):
        return self._value


class StringNumberSpinBox(SpinBox):
    value_changed = Signal(int)

    def __init__(self, *args, string_number: int, minimum=4, maximum=8, **kwargs):
        super(StringNumberSpinBox, self).__init__(
            *args, minimum=minimum, maximum=maximum, **kwargs
        )

        self.set(string_number)

        self.valueChanged.connect(self.value_changed.emit)

    def set(self, value: int):
        self._value = value

        with block_signal([self]):
            self.setValue(value)


class OctaveSpinBox(SpinBox):
    value_changed = Signal(int)

    def __init__(self, *args, octave: int, minimum=4, maximum=10, **kwargs):
        super(OctaveSpinBox, self).__init__(
            *args, minimum=minimum, maximum=maximum, **kwargs
        )

        self.set(octave)

        self.valueChanged.connect(self.handle_octave_change)

    def set(self, octave: int):
        self._value = octave

        with block_signal([self]):
            self.setValue(self._value)

    def handle_octave_change(self, octave: int):
        self._value = octave

        self.value_changed.emit(octave)


class BpmSpinBox(SpinBox):
    value_changed = Signal(Bpm)

    def __init__(
        self, *args, bpm: Bpm = Bpm(value=90), minimum=20, maximum=300, **kwargs
    ):
        super(BpmSpinBox, self).__init__(
            *args, minimum=minimum, maximum=maximum, **kwargs
        )

        self.set(bpm)

        self.valueChanged.connect(self.handle_value_change)

    def set(self, bpm: Bpm):
        self._value = bpm

        with block_signal([self]):
            self.setValue(bpm.value)

    def handle_value_change(self, value):
        if value > self.minimum() and value < self.maximum():
            self._value = Bpm(value=value)

            self.value_changed.emit(self.value)
