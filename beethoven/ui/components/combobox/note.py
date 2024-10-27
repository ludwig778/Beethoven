import logging
from typing import List, Union

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QComboBox

from beethoven.models import Note
from beethoven.ui.utils import block_signal

logger = logging.getLogger("combobox.note")


class BaseNoteComboBox(QComboBox):
    value_changed = Signal(Note)

    def __init__(self, *args, note: Note | None, **kwargs):
        # super(NoteWithOctaveComboBox, self).__init__(*args, **kwargs)
        super(BaseNoteComboBox, self).__init__(*args, **kwargs)

        self.setAttribute(Qt.WA_StyledBackground)

        self.addItems([str(n) for n in self.available_notes])

        self.set(note)

        self.currentIndexChanged.connect(self.handle_note_change)

    def handle_note_change(self, value):
        self.value = self.available_notes[value]

        logger.debug(str(self.value))

        self.value_changed.emit(self.value)


class NoteComboBox(BaseNoteComboBox):
    available_notes = Note.parse_list("A,A#,B,C,C#,D,D#,E,F,F#,G,G#")

    """
    def __init__(self, *args, note: Note, **kwargs):
        super(NoteComboBox, self).__init__(*args, **kwargs)

        self.setAttribute(Qt.WA_StyledBackground)

        self.addItems([str(n) for n in self.available_notes])

        self.set(note)

        self.currentIndexChanged.connect(self.handle_note_change)
    """

    def set(self, note: Note):
        logger.debug(str(note))

        self.value = note

        with block_signal([self]):
            self.setCurrentIndex(self.available_notes.index(note.remove_octave()))


class NoteWithOctaveComboBox(BaseNoteComboBox):
    value_changed = Signal(object)
    available_notes: List[Union[str, Note]] = []

    for o in range(10, -1, -1):
        available_notes += reversed(
            Note.parse_list(f"C{o},C#{o},D{o},D#{o},E{o},F{o},F#{o},G{o},G#{o},A{o},A#{o},B{o}")
        )

    available_notes.append("")

    def set(self, note: Note | None):
        logger.debug(str(note))

        self.value = note

        with block_signal([self]):
            self.setCurrentText(str(self.value or ""))
