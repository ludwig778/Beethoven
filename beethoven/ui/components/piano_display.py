from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QStyle, QStyleOption, QWidget

from beethoven.ui.utils import color_from_hsl


class PianoDisplay(QWidget):
    white_key_color: QColor = QColor(color_from_hsl(45, 15, 90).hex)
    black_key_color: QColor = QColor(color_from_hsl(0, 0, 15).hex)
    seperator_color: QColor = QColor(color_from_hsl(45, 10, 75).hex)
    scale_note_dot_color: QColor = QColor(color_from_hsl(210, 70, 60).hex)
    chord_note_dot_color: QColor = QColor(color_from_hsl(360, 70, 60).hex)
    note_dot_size: int = 20

    black_key_width_ratio = 0.6
    black_key_width_ratio = 0.7
    black_key_height_ratio = 0.6

    white_key_note_height_ratio = 0.8
    black_key_note_height_ratio = 0.4

    starts_with_a = True
    starts_with_a = False
    ends_with_c = False
    octaves = 2
    black_key_offsets = {
        0: 0.65,
        1: 0.35,
        3: 0.70,
        4: 0.5,
        5: 0.30,
    }
    white_key_semitones = {
        0: 0,
        1: 2,
        2: 4,
        3: 5,
        4: 7,
        5: 9,
        6: 11,
    }

    def __init__(self, *args, harmony_item, chord_item, **kwargs):
        super(PianoDisplay, self).__init__(*args, **kwargs)

        self.scale = harmony_item.scale
        self.chord = chord_item.as_chord(self.scale)

        self.setMinimumSize(250, 140)
        self.setMinimumSize(600, 170)

    def paintEvent(self, event):
        painter = QPainter()
        opt = QStyleOption()

        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        opt.initFrom(self)

        self.paint_keyboard(painter)
        self.paint_notes(painter)

        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

        painter.end()

    def update_items(self, harmony_item, chord_item):
        self.scale = harmony_item.scale
        self.chord = chord_item.as_chord(self.scale)

        if self.isVisible():
            self.update()

    @property
    def keys(self):
        keys = self.octaves * 7

        if self.starts_with_a:
            keys += 2

        if self.ends_with_c:
            keys += 1

        return keys

    def paint_keyboard(self, painter: QPainter):
        width = self.width()
        height = self.height()

        painter.setBrush(self.white_key_color)
        painter.setPen(self.white_key_color)

        painter.drawRect(0, 0, width, height)

        painter.setBrush(self.seperator_color)
        painter.setPen(self.seperator_color)

        keys = self.keys
        width_fraction = width / keys
        for i in range(0, keys):
            line_pos = i * width_fraction

            painter.drawLine(line_pos, 0, line_pos, height)

        painter.setBrush(self.black_key_color)
        painter.setPen(self.seperator_color)

        for i in range(0, keys):
            line_pos = i * width_fraction

            if self.starts_with_a:
                i -= 2
            black_key_offset = self.black_key_offsets.get(i % 7)

            if not black_key_offset:
                continue

            if line_pos + width_fraction >= width:
                break

            black_key_width = width_fraction * self.black_key_width_ratio

            painter.drawRect(
                int(line_pos + width_fraction - (black_key_width * black_key_offset)),
                0,
                int(black_key_width),
                int(height * self.black_key_height_ratio),
            )

    def paint_notes(self, painter: QPainter):
        width = self.width()
        height = self.height()

        keys = self.keys
        if self.starts_with_a:
            keys += 2

        chord_note_names = {n.index: str(n.remove_octave()) for n in self.chord.notes}
        scale_note_names = {n.index: str(n.remove_octave()) for n in self.scale.notes}

        keys = self.keys
        width_fraction = width / keys

        for i in range(0, keys):
            line_pos = i * width_fraction

            if self.starts_with_a:
                i -= 2

            semitones = self.white_key_semitones[i % 7]

            chord_note = chord_note_names.get(semitones)
            scale_note = scale_note_names.get(semitones)

            if chord_note or scale_note:
                if chord_note:
                    painter.setBrush(self.chord_note_dot_color)
                    painter.setPen(self.chord_note_dot_color)
                else:
                    painter.setBrush(self.scale_note_dot_color)
                    painter.setPen(self.scale_note_dot_color)

                painter.drawEllipse(
                    int(line_pos + ((width_fraction - self.note_dot_size) / 2)),
                    int(height * self.white_key_note_height_ratio),
                    self.note_dot_size,
                    self.note_dot_size,
                )

            black_key_offset = self.black_key_offsets.get(i % 7)

            if not black_key_offset:
                continue

            chord_note = chord_note_names.get(semitones + 1)
            scale_note = scale_note_names.get(semitones + 1)

            if chord_note or scale_note:
                if chord_note:
                    painter.setBrush(self.chord_note_dot_color)
                    painter.setPen(self.chord_note_dot_color)
                else:
                    painter.setBrush(self.scale_note_dot_color)
                    painter.setPen(self.scale_note_dot_color)

                painter.drawEllipse(
                    int(
                        line_pos
                        + width_fraction
                        - (self.note_dot_size / 2)
                        + (width_fraction * (0.5 - black_key_offset) * self.black_key_width_ratio)
                    ),
                    int(height * self.black_key_note_height_ratio),
                    self.note_dot_size,
                    self.note_dot_size,
                )
