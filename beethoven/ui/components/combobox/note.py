from logging import getLogger

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QComboBox

from beethoven.models import Note
from beethoven.ui.utils import block_signal

logger = getLogger("combobox.note")


class NoteComboBox(QComboBox):
    value_changed = Signal(Note)
    available_notes = Note.parse_list("A,A#,B,C,C#,D,D#,E,F,F#,G,G#")

    def __init__(self, *args, note: Note, **kwargs):
        super(NoteComboBox, self).__init__(*args, **kwargs)

        self.setAttribute(Qt.WA_StyledBackground)

        self.addItems([str(n) for n in self.available_notes])

        self.set(note)

        self.currentIndexChanged.connect(self.handle_note_change)

    def set(self, note: Note):
        self.value = note

        with block_signal([self]):
            self.setCurrentIndex(self.available_notes.index(note.remove_octave()))

    def handle_note_change(self, value):
        self.value = self.available_notes[value]

        self.value_changed.emit(self.value)
