import logging
from fractions import Fraction

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox, QLabel, QWidget

from beethoven.models import DurationItem
from beethoven.ui.components.spinbox import SpinBox
from beethoven.ui.constants import BASE_DURATIONS
from beethoven.ui.layouts import horizontal_layout
from beethoven.ui.utils import block_signal

logger = logging.getLogger("selectors.duration")


class DurationSelector(QWidget):
    value_changed = Signal(object)
    end_of_bar_label = "End of bar"

    def __init__(self, *args, duration_item: DurationItem, enable_denominator: bool = False, **kwargs):
        super(DurationSelector, self).__init__(*args, **kwargs)

        self.numerator_spinbox = SpinBox(minimum=1, maximum=52)
        self.denominator_spinbox = SpinBox(minimum=1, maximum=52)

        self.duration_unit_combobox = QComboBox()
        self.duration_unit_combobox.addItem(self.end_of_bar_label)
        self.duration_unit_combobox.addItems(list(BASE_DURATIONS.keys()))

        self.numerator_spinbox.valueChanged.connect(self.handle_numerator_change)
        self.denominator_spinbox.valueChanged.connect(self.handle_denominator_change)
        self.duration_unit_combobox.currentTextChanged.connect(self.handle_duration_unit_change)

        self.set(duration_item)

        items_layout = [
            self.numerator_spinbox,
            self.duration_unit_combobox,
        ]
        if enable_denominator:
            items_layout.insert(1, QLabel("/"))
            items_layout.insert(2, self.denominator_spinbox)

        self.setLayout(horizontal_layout(items_layout))  # type: ignore

    def set(self, duration_item: DurationItem):
        self.value = duration_item

        if duration_item.base_duration is None:
            self._set_spinbox_states(False)
            self._set_spinbox_values(Fraction(1, 1))

            self.duration_unit_combobox.setCurrentText(self.end_of_bar_label)
        else:
            self._set_spinbox_states(True)

            for label, default_duration in BASE_DURATIONS.items():
                if duration_item.base_duration == default_duration:
                    break

            self._set_spinbox_values(duration_item.fraction)

            self.duration_unit_combobox.setCurrentText(label)

    def handle_numerator_change(self, numerator):
        if (
            numerator >= self.numerator_spinbox.minimum()
            and numerator <= self.numerator_spinbox.maximum()
        ):
            self.update_duration_item(numerator=numerator)

    def handle_denominator_change(self, denominator):
        if (
            denominator >= self.denominator_spinbox.minimum()
            and denominator <= self.denominator_spinbox.maximum()
        ):
            self.update_duration_item(denominator=denominator)

    def handle_duration_unit_change(self, value):
        if value == self.end_of_bar_label:
            self._set_spinbox_states(False)

            self.update_duration_item(base_duration=None)
        else:
            self._set_spinbox_states(True)

            self.update_duration_item(base_duration=BASE_DURATIONS.get(value))

    def update_duration_item(self, numerator=None, denominator=None, base_duration=None):
        self.value = DurationItem(
            numerator=numerator or self.value.numerator,
            denominator=denominator or self.value.denominator,
            base_duration=base_duration or self.value.base_duration,
        )

        self.value_changed.emit(self.value)

    def _set_spinbox_values(self, fraction: Fraction):
        with block_signal([self.numerator_spinbox, self.denominator_spinbox]):
            self.numerator_spinbox.setValue(fraction.numerator)
            self.denominator_spinbox.setValue(fraction.denominator)

    def _set_spinbox_states(self, state: bool):
        self.numerator_spinbox.setEnabled(state)
        self.denominator_spinbox.setEnabled(state)

        if not state:
            with block_signal([self.numerator_spinbox, self.denominator_spinbox]):
                self.numerator_spinbox.setValue(1)
                self.denominator_spinbox.setValue(1)
