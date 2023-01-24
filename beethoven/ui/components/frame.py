from typing import List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel

from beethoven.models import Chord, Note, Scale, Degree
from beethoven.ui.layouts import Stretch, vertical_layout
from beethoven.utils.alterations import get_degree_alteration_str_from_int


class FramedText(QFrame):
    def __init__(self, *args, upper_text: str, **kwargs):
        super(FramedText, self).__init__(*args, **kwargs)

        self.setAttribute(Qt.WA_StyledBackground)

        upper_label = QLabel(upper_text)
        upper_label.setAlignment(Qt.AlignCenter)  # type: ignore
        upper_label.setObjectName("upper_text")

        self.lower_label = QLabel()
        self.lower_label.setAlignment(Qt.AlignCenter)  # type: ignore
        self.lower_label.setObjectName("lower_text")

        self.setLayout(vertical_layout([upper_label, self.lower_label, Stretch()]))

    def setText(self, text: str):
        self.lower_label.setText(text)

    def clear(self):
        self.lower_label.setText("")


class FramedNotes(FramedText):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("upper_text", "Notes :")

        super(FramedNotes, self).__init__(*args, **kwargs)

    def set_notes(self, notes: List[Note]):
        if len(notes) <= 6:
            self.setText(" ".join([str(note) for note in notes]))
        else:
            self.setText("Too much notes")


class FramedChord(FramedText):
    def __init__(self, *args, **kwargs):
        super(FramedChord, self).__init__(*args, upper_text="Chord :", **kwargs)

    def set_chord(self, chord: Chord):
        self.setText(f"{str(chord.root)} {chord.name}")


class FramedDegree(FramedText):
    def __init__(self, *args, **kwargs):
        super(FramedDegree, self).__init__(*args, upper_text="Degree :", **kwargs)

    def set_degree(self, degree: Degree):
        self.setText(
            f"{get_degree_alteration_str_from_int(degree.alteration)}{degree.name}"
        )


class FramedScale(FramedText):
    def __init__(self, *args, **kwargs):
        super(FramedScale, self).__init__(*args, upper_text="Scale :", **kwargs)

    def set_scale(self, scale: Scale):
        self.setText(f"{str(scale.tonic)} {scale.name}")
