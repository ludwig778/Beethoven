from typing import List, Optional, Tuple

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QWidget

from beethoven.helpers.sequencer import get_chord_from_items
from beethoven.models import Chord, Degree, Note, Scale
from beethoven.ui.layouts import Spacing, Stretch, horizontal_layout, vertical_layout
from beethoven.ui.models import ChordItem, HarmonyItem
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

    def set_text(self, text: str):
        self.lower_label.setText(text)

    def clear(self):
        self.lower_label.setText("")


class FramedNote(FramedText):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("upper_text", "Notes :")

        super(FramedNote, self).__init__(*args, **kwargs)

    def set_notes(self, notes: List[Note], separator: str = " "):
        if len(notes) <= 6:
            self.set_text(separator.join([str(note) for note in notes]))
        else:
            self.set_text("Too much notes")


class FramedChord(FramedText):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("upper_text", "Chord :")

        super(FramedChord, self).__init__(*args, **kwargs)

    def set_chord(self, chord: Chord):
        self.set_text(f"{str(chord.root)} {chord.name}")

    def set_chords(self, chords: List[Chord], separator: str = " "):
        self.set_text(
            separator.join([f"{str(chord.root)} {chord.name}" for chord in chords])
        )


class FramedDegree(FramedText):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("upper_text", "Degree :")

        super(FramedDegree, self).__init__(*args, **kwargs)

    def set_degree(self, degree: Degree):
        self.set_text(
            f"{get_degree_alteration_str_from_int(degree.alteration)}{degree.name}"
        )

    def set_degrees(self, degrees: List[Degree], separator: str = " "):
        self.set_text(
            separator.join(
                [
                    f"{get_degree_alteration_str_from_int(degree.alteration)}{degree.name}"
                    for degree in degrees
                ]
            )
        )


class FramedScale(FramedText):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("upper_text", "Scale :")

        super(FramedScale, self).__init__(*args, **kwargs)

    def set_scale(self, scale: Scale):
        self.set_text(f"{str(scale.tonic)} {scale.name}")


class HarmonyChordItemFrames(QWidget):
    def __init__(self, *args, **kwargs):
        super(HarmonyChordItemFrames, self).__init__(*args, **kwargs)

        self.scale_root_frame = FramedNote(upper_text="Scale Roots :")
        self.chord_frame = FramedChord(upper_text="Chords :")
        self.chord_root_frame = FramedText(upper_text="Chord Degrees :")

        self.scale_root_frame.setFixedWidth(115)
        self.chord_root_frame.setFixedWidth(140)

        self.setLayout(
            horizontal_layout(
                [
                    Spacing(size=5),
                    self.scale_root_frame,
                    Spacing(size=5),
                    self.chord_frame,
                    Spacing(size=5),
                    self.chord_root_frame,
                    Spacing(size=5),
                ]
            ),
        )

    def update_frames(
        self,
        current_items: Tuple[HarmonyItem, ChordItem],
        next_items: Optional[Tuple[HarmonyItem, ChordItem]] = None,
        separator: str = " \u2794 ",
    ):
        scale_roots = [current_items[0].scale.tonic]
        chords = [get_chord_from_items(*current_items)[0]]
        roots = [str(current_items[1].root)]

        if next_items:
            if current_items[0].scale.tonic != next_items[0].scale.tonic:
                scale_roots.append(next_items[0].scale.tonic)

            chords.append(get_chord_from_items(*next_items)[0])
            roots.append(str(next_items[1].root))

        self.scale_root_frame.set_notes(scale_roots, separator=separator)
        self.chord_frame.set_chords(chords, separator=separator)
        self.chord_root_frame.set_text(separator.join(roots))
