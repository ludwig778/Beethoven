from itertools import chain, count
from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QPainter, QPixmap
from PySide6.QtWidgets import QStyle, QStyleOption, QWidget

from beethoven.settings import TuningSetting
from beethoven.ui.utils import color_from_hsl, resource_path


class GuitarDisplay(QWidget):
    updated = Signal()

    bridge_color: QColor = QColor(color_from_hsl(0, 0, 25).hex)
    bridge_border_color: QColor = QColor(color_from_hsl(0, 0, 5).hex)

    fret_color: QColor = QColor(color_from_hsl(0, 0, 47).hex)
    fret_border_color: QColor = QColor(color_from_hsl(0, 0, 40).hex)

    string_color: QColor = QColor(color_from_hsl(240, 20, 65).hex)
    string_border_color: QColor = QColor(color_from_hsl(240, 20, 60).hex)

    fretboard_image_path: Path = resource_path("img/maple.png")
    dot_color: QColor = QColor(color_from_hsl(0, 0, 35).hex)

    note_dot_text_color: QColor = QColor(color_from_hsl(360, 100, 96).hex)
    scale_note_dot_color: QColor = QColor(color_from_hsl(210, 70, 60).hex)
    chord_note_dot_color: QColor = QColor(color_from_hsl(360, 70, 60).hex)

    fret_width: int = 4
    string_width: int = 2
    string_height: int = 32
    bridge_start_width: int = 10
    bridge_width: int = 14
    dot_size: int = 20
    note_dot_size: int = 22
    fretboard_end_offset: int = 10
    min_fret: int = 12
    max_fret: int = 24

    def __init__(self, *args, tuning: TuningSetting, harmony_item, chord_item, **kwargs):
        super(GuitarDisplay, self).__init__(*args, **kwargs)

        self.scale = harmony_item.scale
        self.chord = chord_item.as_chord(self.scale)

        self.tuning = tuning

        self.string_num: int = 6
        self.fret_num: int = 12

        self.setMinimumWidth(700)
        self.setFixedHeight(self.string_height * len(self.tuning.notes))

    def update_items(self, harmony_item, chord_item):
        self.scale = harmony_item.scale
        self.chord = chord_item.as_chord(self.scale)

        if self.isVisible():
            self.update()

    def update_tuning(self, tuning):
        self.tuning = tuning

        if self.isVisible():
            self.update()

    def paintEvent(self, event):
        painter = QPainter()
        opt = QStyleOption()

        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        opt.initFrom(self)

        self.setFixedHeight(self.string_height * len(self.tuning.notes))

        self.paint_fretboard(painter)
        self.paint_strings(painter)
        self.paint_notes(painter)

        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

        painter.end()

        self.updated.emit()

    @property
    def bridge_start(self):
        return self.bridge_start_width + self.bridge_width

    @property
    def fret_spacing(self):
        return (self.width() - self.bridge_start - self.fretboard_end_offset) / self.fret_num

    def paint_fretboard(self, painter: QPainter):
        painter.drawPixmap(self.rect(), QPixmap(self.fretboard_image_path))

        fret_spacing = self.fret_spacing

        dot_offset = (fret_spacing + self.dot_size + self.fret_width) / 2
        half_dot_size = self.dot_size / 2
        height_fraction = self.height() / 7

        for fret_index, fret_pos in self.fret_position_iterator:
            if not fret_index:
                painter.setBrush(self.bridge_color)
                painter.setPen(self.bridge_border_color)

                painter.drawRect(fret_pos - self.bridge_width, 0, self.bridge_width, self.height())

                continue
            else:
                painter.setBrush(self.fret_color)
                painter.setPen(self.fret_border_color)

                painter.drawRect(fret_pos - self.fret_width, 0, self.fret_width, self.height())

            if fret_index % 12 not in [0, 3, 5, 7, 9]:
                continue

            painter.setBrush(self.dot_color)
            painter.setPen(self.dot_color)

            dot_pos = int(fret_pos - dot_offset)

            if fret_index % 12 in [0]:
                painter.drawEllipse(
                    dot_pos, int(height_fraction * 2 - half_dot_size), self.dot_size, self.dot_size
                )
                painter.drawEllipse(
                    dot_pos, int(height_fraction * 5 - half_dot_size), self.dot_size, self.dot_size
                )
            else:
                painter.drawEllipse(
                    dot_pos, int(height_fraction * 7 / 2 - half_dot_size), self.dot_size, self.dot_size
                )

    @property
    def fret_position_iterator(self):
        bridge_start = self.bridge_start
        fret_spacing = self.fret_spacing

        return chain(
            ((0, bridge_start),),
            zip(range(1, self.fret_num + 1), count(bridge_start + fret_spacing, fret_spacing)),
        )

    @property
    def string_position_iterator(self):
        return zip(reversed(self.tuning.notes), count(self.string_height / 2, self.string_height))

    def paint_strings(self, painter: QPainter):
        painter.setBrush(self.string_color)
        painter.setPen(self.string_border_color)

        string_offset = self.string_width / 2

        for _, string_pos in self.string_position_iterator:
            painter.drawRect(0, string_pos - string_offset, self.width(), self.string_width)

    def paint_notes(self, painter: QPainter):
        dot_offset = (self.fret_spacing + self.note_dot_size + self.fret_width) / 2
        half_dot_size = self.dot_size / 2

        chord_note_names = {n.index: str(n.remove_octave()) for n in self.chord.notes}
        scale_note_names = {n.index: str(n.remove_octave()) for n in self.scale.notes}

        for string_note, string_pos in self.string_position_iterator:
            string_note_index = string_note.index
            string_pos -= half_dot_size

            for fret_index, fret_pos in self.fret_position_iterator:
                chord_note = chord_note_names.get((string_note_index + fret_index) % 12)
                scale_note = scale_note_names.get((string_note_index + fret_index) % 12)

                note = chord_note or scale_note

                if not note:
                    continue

                if fret_index == 0:
                    fret_pos -= (self.bridge_width + self.note_dot_size) / 2
                else:
                    fret_pos -= dot_offset

                if chord_note:
                    painter.setBrush(self.chord_note_dot_color)
                    painter.setPen(self.chord_note_dot_color)
                elif scale_note:
                    painter.setBrush(self.scale_note_dot_color)
                    painter.setPen(self.scale_note_dot_color)

                painter.drawEllipse(fret_pos, string_pos, self.note_dot_size, self.note_dot_size)

                painter.setBrush(self.note_dot_text_color)
                painter.setPen(self.note_dot_text_color)

                painter.drawText(
                    fret_pos,
                    string_pos,
                    self.note_dot_size,
                    self.note_dot_size,
                    Qt.AlignHCenter | Qt.AlignCenter,
                    str(note),
                )
