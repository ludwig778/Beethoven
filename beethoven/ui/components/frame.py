from typing import List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit

from beethoven.models import Chord, Note, Scale
from beethoven.models.degree import Degree
from beethoven.utils.alterations import get_degree_alteration_str_from_int


class FramedLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super(FramedLineEdit, self).__init__(*args, **kwargs)

        self.setAlignment(Qt.AlignCenter)
        self.setReadOnly(True)


class FramedNotes(FramedLineEdit):
    def set_notes(self, notes: List[Note]):
        if len(notes) <= 6:
            self.setText(" ".join([str(note) for note in notes]))
        else:
            self.setText("Too much notes")


class FramedChord(FramedNotes):
    def set_chord(self, chord: Chord):
        self.setText(f"{str(chord.root)} {chord.name}")


class FramedDegree(FramedNotes):
    def set_degree(self, degree: Degree):
        self.setText(f"{get_degree_alteration_str_from_int(degree.alteration)}{degree.name}")


class FramedScale(FramedNotes):
    def set_scale(self, scale: Scale):
        self.setText(f"{str(scale.tonic)} {scale.name}")
