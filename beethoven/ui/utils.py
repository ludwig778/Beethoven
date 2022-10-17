from contextlib import contextmanager
from typing import Callable, List, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QWidget

from beethoven import controllers
from beethoven.adapters.midi import MidiAdapter
from beethoven.sequencer.players.base import BasePlayer
from beethoven.sequencer.players.registry import RegisteredPlayer
from beethoven.ui.models import ChordItem, HarmonyItem, HarmonyItems
from beethoven.ui.settings import PlayerSetting


@contextmanager
def block_signal(widgets: List[QWidget]):
    for widget in widgets:
        widget.blockSignals(True)
    try:
        yield
    finally:
        for widget in widgets:
            widget.blockSignals(False)


def set_object_name(widget: QWidget, object_name: Optional[str] = None, **kwargs):
    if object_name:
        widget.setObjectName(object_name)


def get_checked_items(list_widget: QListWidget) -> List[QListWidgetItem]:
    checked_items = []

    for index in range(list_widget.count()):
        item = list_widget.item(index)

        if item.checkState() == Qt.Checked:
            checked_items.append(item)

    return checked_items


# TODO: Set as an helper, maybe ?
def setup_players(
    midi_adapter: MidiAdapter, player_settings: List[PlayerSetting]
) -> List[BasePlayer]:
    players = []

    for player_setting in player_settings:
        player_class = RegisteredPlayer.get_instrument_style(
            player_setting.instrument_name, player_setting.instrument_style
        )

        if not player_class:
            continue

        player = player_class()

        if player_setting.output_name:
            player.setup_midi(
                output=midi_adapter.open_output(player_setting.output_name),
                channel=player_setting.channel,
            )

        players.append(player)

    return players


def run_method_on_widgets(
    method: Callable, widgets: List[QWidget], *args, **kwargs
) -> None:
    for widget in widgets:
        method(widget, *args, **kwargs)


def get_default_chord_item() -> ChordItem:
    return ChordItem(root=controllers.degree.parse("I"), name="")


def get_default_harmony_item() -> HarmonyItem:
    return HarmonyItem(
        scale=controllers.scale.parse("C4_major"),
        chord_items=[get_default_chord_item()],
    )


def get_default_harmony_items() -> HarmonyItems:
    return HarmonyItems(
        items=[
            HarmonyItem(
                scale=controllers.scale.parse("C4_major"),
                chord_items=[get_default_chord_item()],
            )
        ]
    )
