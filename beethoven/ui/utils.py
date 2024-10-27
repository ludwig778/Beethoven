import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, List

from colour import Color
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QWidget

from beethoven.adapters.midi import MidiAdapter
from beethoven.models import (ChordItem, Degree, Duration, DurationItem,
                              HarmonyItem, Scale)
# from beethoven.sequencer.players import BasePlayer
# from beethoven.sequencer.registry import RegisteredPlayer
# from beethoven.settings import PlayerSetting
from beethoven.ui.constants import DEFAULT_BPM, DEFAULT_TIME_SIGNATURE


@contextmanager
def block_signal(widgets: List):
    for widget in widgets:
        widget.blockSignals(True)
    try:
        yield
    finally:
        for widget in widgets:
            widget.blockSignals(False)


def get_checked_items(list_widget: QListWidget) -> List[QListWidgetItem]:
    checked_items = []

    for index in range(list_widget.count()):
        item = list_widget.item(index)

        if item.checkState() == Qt.Checked:
            checked_items.append(item)

    return checked_items


def run_method_on_widgets(method: Callable, widgets: List[QWidget], *args, **kwargs) -> None:
    for widget in widgets:
        method(widget, *args, **kwargs)


def get_default_chord_item() -> ChordItem:
    return ChordItem(root=Degree.parse("I"), name="", duration_item=DurationItem())


def get_default_harmony_item() -> HarmonyItem:
    return HarmonyItem(
        scale=Scale.parse("C4_major"),
        chord_items=[get_default_chord_item()],
        bpm=DEFAULT_BPM,
        time_signature=DEFAULT_TIME_SIGNATURE,
    )


"""
        chord_items=[
            ChordItem(
                #root=Degree.parse("bbII"),
                root=Degree.parse("II"),
                #root=Degree.parse("##II"),
                #root=Degree.parse("I"),
                name="7",
                duration_item=DurationItem(),
                #inversion=2,
            ),
            ChordItem(
                root=Degree.parse("V"),
                name="",
                duration_item=DurationItem(),
            ),
            ChordItem(
                root=Degree.parse("I"),
                name="",
                duration_item=DurationItem(),
            ),
        ],
    )

def get_default_harmony_items() -> List[HarmonyItem]:
    return [get_default_harmony_item(), get_default_harmony_item()]
"""


def get_default_harmony_items() -> List[HarmonyItem]:
    # return [get_default_harmony_item()]
    return [
        HarmonyItem(
            scale=Scale.parse("C4_major"),
            bpm=DEFAULT_BPM,
            time_signature=DEFAULT_TIME_SIGNATURE,
            chord_items=[
                ChordItem(
                    root=Degree.parse("II"),
                    name="",
                    duration_item=DurationItem(base_duration=Duration.parse("4")),
                ),
                ChordItem(
                    root=Degree.parse("V"),
                    name="",
                    duration_item=DurationItem(),
                ),
                ChordItem(
                    root=Degree.parse("I"),
                    name="",
                    duration_item=DurationItem(),
                ),
            ],
        ),
        HarmonyItem(
            scale=Scale.parse("G4_mixolydian"),
            bpm=DEFAULT_BPM,
            time_signature=DEFAULT_TIME_SIGNATURE,
            chord_items=[
                ChordItem(
                    root=Degree.parse("IV"),
                    name="",
                    duration_item=DurationItem(),
                ),
                ChordItem(
                    root=Degree.parse("VI"),
                    name="",
                    duration_item=DurationItem(),
                ),
                ChordItem(
                    root=Degree.parse("III"),
                    name="",
                    duration_item=DurationItem(),
                ),
            ],
        ),
    ]


def get_harmony_items_from_list(data_items):
    return [HarmonyItem.from_dict(item) for item in data_items]


def get_harmony_items_to_dict(harmony_items):
    return [item.dict() for item in harmony_items]


def resource_path(relative_path: str) -> Path:
    try:
        base_path = Path(sys._MEIPASS)
    except Exception:
        base_path = Path(".") / "beethoven/ui/resources"

    return base_path / relative_path


def color_from_hsl(hue: int = 0, saturation: int = 0, lightness: int = 0) -> Color:
    return Color(hsl=(hue / 360, saturation / 100, lightness / 100))
