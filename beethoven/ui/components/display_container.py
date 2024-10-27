import logging
from typing import TypeVar

from PySide6.QtWidgets import QWidget

from beethoven.models import ChordItem, HarmonyItem
from beethoven.ui.components.buttons import PushPullButton
from beethoven.ui.dialogs.guitar_display import GuitarDisplayDialog
from beethoven.ui.dialogs.piano_display import PianoDisplayDialog
from beethoven.ui.dialogs.player import PlayerDialog
from beethoven.ui.layouts import vertical_layout
from beethoven.ui.managers import AppManager

logger = logging.getLogger("app.compose")

T = TypeVar("T", HarmonyItem, ChordItem)


class DisplayContainerWidget(QWidget):
    def __init__(
        self, *args, manager: AppManager, harmony_item: HarmonyItem, chord_item: ChordItem, parent: QWidget | None = None, **kwargs
    ):
        super(DisplayContainerWidget, self).__init__(*args, **kwargs)

        self.manager = manager

        self.guitar_display_button = PushPullButton("Fretboard", object_name="guitar_button")
        self.piano_display_button = PushPullButton("Keyboard", object_name="piano_button")
        self.players_display_button = PushPullButton("Players", object_name="players_button")

        self.guitar_display_dialog = GuitarDisplayDialog(
            manager=manager, harmony_item=harmony_item, chord_item=chord_item, parent=parent
        )
        self.piano_display_dialog = PianoDisplayDialog(
            harmony_item=harmony_item, chord_item=chord_item, parent=parent
        )
        self.players_dialog = PlayerDialog(manager=manager, parent=parent)

        self.guitar_display_button.connect_to_dialog(self.guitar_display_dialog)
        self.piano_display_button.connect_to_dialog(self.piano_display_dialog)
        self.players_display_button.connect_to_dialog(self.players_dialog)

        self.setLayout(
            vertical_layout(
                [
                    self.guitar_display_button,
                    self.piano_display_button,
                    self.players_display_button,
                ],
            )
        )

    def update_items(self, harmony_item: HarmonyItem, chord_item: ChordItem):
        self.guitar_display_dialog.update_items(harmony_item, chord_item)
        self.piano_display_dialog.update_items(harmony_item, chord_item)
