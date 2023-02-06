from contextlib import contextmanager
from typing import Callable, List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QListWidget, QListWidgetItem, QWidget

from beethoven.adapters.midi import MidiAdapter
from beethoven.models import Degree, Scale
from beethoven.sequencer.players.base import BasePlayer
from beethoven.sequencer.players.registry import RegisteredPlayer
from beethoven.settings import PlayerSetting
from beethoven.ui.components.buttons import PushPullButton
from beethoven.ui.constants import DEFAULT_BPM, DEFAULT_TIME_SIGNATURE
from beethoven.ui.models import ChordItem, DurationItem, HarmonyItem


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
    return ChordItem(
        root=Degree.parse("I"), name="", duration_item=DurationItem()
    )


def get_default_harmony_item() -> HarmonyItem:
    return HarmonyItem(
        scale=Scale.parse("C4_major"),
        chord_items=[
            ChordItem(
                root=Degree.parse("II"),
                name="",
                duration_item=DurationItem(),
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
        # chord_items=[get_default_chord_item()],
        bpm=DEFAULT_BPM,
        time_signature=DEFAULT_TIME_SIGNATURE,
    )


def get_default_harmony_items() -> List[HarmonyItem]:
    return [get_default_harmony_item(), get_default_harmony_item()]


def get_harmony_items_from_list(data_items):
    return [HarmonyItem.from_dict(item) for item in data_items]


def get_harmony_items_to_dict(harmony_items):
    return [item.dict() for item in harmony_items]


def connect_push_pull_button_and_dialog(
    push_pull_button: PushPullButton, dialog: QDialog
):
    def handle_push_pull_button_toggle(value):
        if value:
            dialog.show()
        else:
            with block_signal([dialog]):
                dialog.close()

    push_pull_button.toggled.connect(handle_push_pull_button_toggle)
    dialog.finished.connect(push_pull_button.toggle)
