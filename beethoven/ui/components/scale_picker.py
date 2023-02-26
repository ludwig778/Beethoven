from dataclasses import replace

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from beethoven.models import Scale
from beethoven.ui.components.combobox import NoteComboBox, ScaleComboBox
from beethoven.ui.components.spinbox import OctaveSpinBox
from beethoven.ui.layouts import horizontal_layout
from beethoven.ui.utils import block_signal


class ScalePicker(QWidget):
    value_changed = Signal(Scale)

    def __init__(self, *args, scale: Scale, **kwargs):
        super(ScalePicker, self).__init__(*args, **kwargs)

        self.tonic_combobox = NoteComboBox(note=scale.tonic.remove_octave())
        self.name_combobox = ScaleComboBox(scale_name=scale.name)
        self.octave_spinbox = OctaveSpinBox(minimum=2, octave=scale.tonic.octave or 4, maximum=8)

        self.set(scale)

        self.tonic_combobox.value_changed.connect(self.handle_tonic_change)
        self.name_combobox.value_changed.connect(self.handle_scale_name_change)
        self.octave_spinbox.value_changed.connect(self.handle_octave_change)

        self.setLayout(
            horizontal_layout(
                [
                    self.tonic_combobox,
                    self.name_combobox,
                    self.octave_spinbox,
                ]
            )
        )

    def set(self, scale: Scale):
        self.value = scale

        with block_signal(
            [
                self.tonic_combobox,
                self.name_combobox,
                self.octave_spinbox,
            ]
        ):
            self.tonic_combobox.set(scale.tonic.remove_octave())
            self.name_combobox.set(scale.name)

            if scale.tonic.octave:
                self.octave_spinbox.set(scale.tonic.octave)

    def handle_tonic_change(self, tonic):
        self.update_scale(tonic=tonic)

    def handle_scale_name_change(self, scale_name):
        self.update_scale(scale_name=scale_name)

    def handle_octave_change(self, octave):
        self.update_scale(octave=octave)

    def update_scale(self, tonic=None, scale_name=None, octave=None):
        tonic = replace(tonic or self.value.tonic, octave=octave or self.value.tonic.octave)

        self.value = Scale.build(tonic=tonic, name=scale_name or self.value.name)

        self.value_changed.emit(self.value)
