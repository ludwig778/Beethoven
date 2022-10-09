from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox

import beethoven.controllers.note as note_controller
from beethoven import indexes
from beethoven.helpers.note import remove_note_octave
from beethoven.models.note import Note
from beethoven.ui.constants import DEFAULT_MIDI_OUTPUT
from beethoven.ui.managers import AppManager
from beethoven.ui.settings import TuningSettings
from beethoven.ui.utils import set_object_name


class MidiChannelComboBox(QComboBox):
    def __init__(self, *args, value: int, **kwargs):
        super(MidiChannelComboBox, self).__init__(*args, **kwargs)

        set_object_name(self, **kwargs)

        for i in range(16):
            self.addItem(str(i))

        self.setCurrentText(str(value))


class MidiInputComboBox(QComboBox):
    def __init__(self, *args, manager: AppManager, value: str, **kwargs):
        super(MidiInputComboBox, self).__init__(*args, **kwargs)

        set_object_name(self, **kwargs)

        self.manager = manager

        self.setup_items()

        self.setCurrentText(str(value))

    def setup_items(self):
        self.clear()

        self.addItem(DEFAULT_MIDI_OUTPUT)

        for input_name in self.manager.adapters.midi.available_inputs:
            self.addItem(input_name)


class MidiOutputComboBox(QComboBox):
    def __init__(self, *args, manager: AppManager, value: str, **kwargs):
        super(MidiOutputComboBox, self).__init__(*args, **kwargs)

        set_object_name(self, **kwargs)

        self.manager = manager

        self.setup_items()

        self.setCurrentText(str(value))

    def setup_items(self):
        self.addItem(DEFAULT_MIDI_OUTPUT)

        for output_name in self.manager.adapters.midi.outputs:
            self.addItem(output_name)


class NoteComboBox(QComboBox):
    note_changed = Signal(Note)
    AVAILABLE_NOTES = note_controller.parse_list("A,A#,B,C,C#,D,D#,E,F,F#,G,G#")

    def __init__(self, *args, selected_note: Note, **kwargs):
        super(NoteComboBox, self).__init__(*args, **kwargs)

        set_object_name(self, **kwargs)

        for note in self.AVAILABLE_NOTES:
            self.addItem(str(note))

        self.set_note(selected_note)

        self.currentTextChanged.connect(self.send_new_note)

    def set_note(self, note: Note):
        self.setCurrentIndex(self.AVAILABLE_NOTES.index(remove_note_octave(note)))

    def get_note(self):
        return self.AVAILABLE_NOTES[self.currentIndex()]

    def send_new_note(self):
        self.note_changed.emit(self.get_note())


class TuningNameComboBox(QComboBox):
    def __init__(self, *args, tuning_settings: TuningSettings, **kwargs):
        super(TuningNameComboBox, self).__init__(*args, **kwargs)

        set_object_name(self, **kwargs)

        self.tuning_settings = tuning_settings

        for tuning_name in self.tuning_settings.tunings.keys():
            self.addItem(tuning_name)

        self.setCurrentIndex(0)

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


class ScaleNameComboBox(QComboBox):
    scale_name_changed = Signal(str)

    def __init__(self, *args, selected_scale_name: str, **kwargs):
        super(ScaleNameComboBox, self).__init__(*args, **kwargs)

        set_object_name(self, **kwargs)

        self.scale_names = [
            scale_data.names[0]
            for scale_data in indexes.scale_index.get_scales_by_label_data(
                ["main_diatonic", "major"]
            )
        ]

        for scale_name in self.scale_names:
            self.addItem(scale_name)

        self.currentTextChanged.connect(self.scale_name_changed.emit)

        self.set_scale_name(selected_scale_name)

    def set_scale_name(self, scale_name: str):
        self.setCurrentIndex(self.scale_names.index(scale_name))

    def get_scale_name(self) -> str:
        return self.scale_names[self.currentIndex()]
