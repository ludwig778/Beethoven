from functools import partial
from typing import Dict, Optional

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from beethoven.ui.components.buttons import PushPullButton
from beethoven.ui.constants import CHORDS_DATA_FLATTEN
from beethoven.ui.layouts import LayoutItems, horizontal_layout, vertical_layout
from beethoven.ui.utils import block_signal


class ChordGridSelector(QWidget):
    value_changed = Signal(str)

    def __init__(self, *args, chord_name: str = "", **kwargs):
        super(ChordGridSelector, self).__init__(*args, **kwargs)

        self.chord_buttons: Dict[str, PushPullButton] = {}
        self._current_button: Optional[PushPullButton] = None

        chords_by_rows = [
            ["maj", "min", "aug", "dim", "power", "dim power", "aug power"],
            ["maj7", "min7", "7", "min7b5", "dim7", "6", "min6"],
            [
                "min maj7",
                "maj7#5",
                "min dim7",
                "dim7 dim3",
                "maj7b5",
                "min maj7b5",
                "7b5",
            ],
            ["sus2", "sus4", "7sus2", "7sus4", "majb5", "dim dim3"],
        ]
        chord_by_names = {chord_data.short_name: chord_data for chord_data in CHORDS_DATA_FLATTEN}

        layout_items: LayoutItems = []

        for chords in chords_by_rows:
            row_items: LayoutItems = []

            for _chord_name in chords:
                assert _chord_name in chord_by_names, f"{_chord_name} unknown"

                button = PushPullButton(_chord_name)
                button.toggled.connect(partial(self.handle_chord_change, button, _chord_name))

                self.chord_buttons[_chord_name] = button

                row_items.append(button)

            layout_items.append(horizontal_layout(row_items))

        self.set(chord_name)

        self.setLayout(vertical_layout(layout_items))

    def set(self, chord_name: str):
        if chord_name == "":
            return

        chord_button = self.chord_buttons[chord_name]

        if self._current_button and self._current_button != chord_button:
            with block_signal([self._current_button]):
                self._current_button.release()

        if not chord_button.pressed:
            with block_signal([chord_button]):
                chord_button.toggle()

        self._current_button = chord_button

    def handle_chord_change(self, button: PushPullButton, chord_name: str, state: bool):
        if state:
            if self._current_button and self._current_button.pressed:
                with block_signal([self._current_button]):
                    self._current_button.release()

            self._current_button = button
        else:
            self._current_button = None

        self.value = chord_name if state else ""

        self.value_changed.emit(self.value)
