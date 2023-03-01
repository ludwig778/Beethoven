from PySide6.QtCore import QAbstractListModel, QRect, QSize, Qt
from PySide6.QtGui import QColor, QFont, QFontMetrics
from PySide6.QtWidgets import QStyle, QStyledItemDelegate

from beethoven.models import ChordItem


class BaseDelegate(QStyledItemDelegate):
    extra_width = 24

    text_color = QColor("#37383c")
    background_color = QColor("#fff")

    highlighted_text_color = QColor("#000")
    highlighted_background_color = QColor("#dedfe0")

    bold_font = QFont("Arial", 12, QFont.Black)  # type: ignore
    normal_font = QFont("Arial", 9, QFont.ExtraBold)  # type: ignore


class HarmonyDelegate(BaseDelegate):
    display_offsets = [12, 19, 14, 18]

    @staticmethod
    def _format_chords(obj):
        return " \u2794 ".join(map(ChordItem.to_simple_string, obj.chord_items))

    def _get_max_width(self, obj):
        return (
            max(
                QFontMetrics(self.bold_font).horizontalAdvance(str(obj.scale)),
                QFontMetrics(self.bold_font).horizontalAdvance(self._format_chords(obj)),
            )
            + self.extra_width
        )

    def sizeHint(self, option, index):
        return QSize(self._get_max_width(index.data(Qt.DisplayRole)), option.rect.height())

    def paint(self, painter, option, index):
        obj = index.data(Qt.DisplayRole)

        left, _, _, height = option.rect.getRect()
        width = self._get_max_width(obj)

        painter.save()

        is_highlighted = option.state & QStyle.State_Selected

        painter.fillRect(
            option.rect,
            self.highlighted_background_color if is_highlighted else self.background_color,
        )
        painter.setPen(self.highlighted_text_color if is_highlighted else self.text_color)

        display_strings = [
            str(obj.scale),
            f"bpm: {obj.bpm.value}",
            f"{obj.time_signature.beats_per_bar}/{obj.time_signature.beat_unit}",
            self._format_chords(obj),
        ]
        display_fonts = [
            self.bold_font,
            self.normal_font,
            self.normal_font,
            self.bold_font,
        ]

        current_offset = 0
        for offset, font, string in zip(self.display_offsets, display_fonts, display_strings):
            current_offset += offset

            painter.setFont(font)
            painter.drawText(
                QRect(left, current_offset - (height / 2), width, height),
                Qt.AlignCenter,
                string,
            )

        painter.restore()


class ChordDelegate(BaseDelegate):
    def _get_max_width(self, obj):
        return (
            max(
                QFontMetrics(self.bold_font).horizontalAdvance(obj.to_simple_string()),
                1,
            )
            + self.extra_width
        )

    def sizeHint(self, option, index):
        return QSize(self._get_max_width(index.data(Qt.DisplayRole)), option.rect.height())

    def paint(self, painter, option, index):
        obj = index.data(Qt.DisplayRole)

        left, _, width, height = option.rect.getRect()

        painter.save()

        is_highlighted = option.state & QStyle.State_Selected

        painter.fillRect(
            option.rect,
            self.highlighted_background_color if is_highlighted else self.background_color,
        )
        painter.setPen(self.highlighted_text_color if is_highlighted else self.text_color)

        chord_rect = (
            QRect(left, 15 - (height / 2), width, height)
            if obj.duration_item.to_string()
            else QRect(left, 25 - (height / 2), width, height)
        )

        painter.setFont(self.bold_font)
        painter.drawText(chord_rect, Qt.AlignCenter, obj.to_simple_string())
        if obj.duration_item.to_string():
            painter.setFont(self.normal_font)
            painter.drawText(
                QRect(left, 35 - (height / 2), width, height),
                Qt.AlignCenter,
                (obj.duration_item.to_string()),
            )

        painter.restore()


class ItemsModel(QAbstractListModel):
    def __init__(self, items):
        super(ItemsModel, self).__init__()

        self.items = items

    def setData(self, index, item, role=Qt.EditRole):
        if role == Qt.EditRole:
            self.items[index.row()] = item

    def insert_item(self, item, row):
        self.items.insert(row, item)

        self.endResetModel()

    def remove(self, index):
        del self.items[index.row()]

        self.endResetModel()

    def set_items(self, items):
        self.items = items

        self.endResetModel()

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            obj = self.items[index.row()]

            return obj

    def __len__(self):
        return len(self.items)

    def rowCount(self, index):
        return len(self)
