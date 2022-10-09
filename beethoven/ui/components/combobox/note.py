from logging import getLogger

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox

import beethoven.controllers.note as note_controller
from beethoven.helpers.note import remove_note_octave
from beethoven.models.note import Note
from beethoven.ui.utils import set_object_name

logger = getLogger("combobox.note")


class NoteComboBox(QComboBox):
    note_changed = Signal(Note)
    AVAILABLE_NOTES = note_controller.parse_list("A,A#,B,C,C#,D,D#,E,F,F#,G,G#")

    def __init__(self, *args, selected_note: Note, **kwargs):
        super(NoteComboBox, self).__init__(*args, **kwargs)

        set_object_name(self, **kwargs)

        for note in self.AVAILABLE_NOTES:
            self.addItem(str(note))

        self.set_note(selected_note)

        self.currentTextChanged.connect(self.on_note_change)

    def set_note(self, note: Note):
        self.setCurrentIndex(self.AVAILABLE_NOTES.index(remove_note_octave(note)))

    def get_note(self):
        return self.AVAILABLE_NOTES[self.currentIndex()]

    def on_note_change(self, note):
        logger.debug(f"change to {note}")

        self.note_changed.emit(note)
