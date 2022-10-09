
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QSpinBox, QWidget

from beethoven import controllers
from beethoven.helpers.note import remove_note_octave
from beethoven.models.scale import Scale
from beethoven.ui.components.combobox import NoteComboBox, ScaleComboBox
from beethoven.ui.layouts import horizontal_layout


class ScalePicker(QWidget):
    scale_changed = Signal(Scale)

    def __init__(self, *args, current_scale: Scale, **kwargs):
        super(ScalePicker, self).__init__(*args, **kwargs)

        self.root_combobox = NoteComboBox(selected_note=remove_note_octave(current_scale.tonic))
        self.name_combobox = ScaleComboBox(selected_scale_name=current_scale.name)
        self.octave_spinbox = QSpinBox()
        self.octave_spinbox.setMinimum(0)
        self.octave_spinbox.setMaximum(10)
        self.octave_spinbox.setValue(current_scale.tonic.octave or 4)

        self.root_combobox.note_changed.connect(self.update_scale)
        self.name_combobox.scale_name_changed.connect(self.update_scale)
        self.octave_spinbox.valueChanged.connect(self.update_scale)

        self.setLayout(
            horizontal_layout([
                self.root_combobox,
                self.name_combobox,
                self.octave_spinbox,
            ])
        )

    def set_scale(self, scale):
        self.root_combobox.set_note(scale.tonic)
        self.name_combobox.set_scale_name(scale.name)
        self.octave_spinbox.setValue(scale.tonic.octave or 4)

    def get_scale(self):
        tonic = self.root_combobox.get_note()
        scale_name = self.name_combobox.get_scale_name()
        octave = self.octave_spinbox.value()

        return controllers.scale.parse(f"{tonic}{octave}_{scale_name}")

    def update_scale(self, *args):
        self.scale_changed.emit(self.get_scale())
