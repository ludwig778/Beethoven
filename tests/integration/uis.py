from functools import partial
from pathlib import Path

from PySide6.QtWidgets import QApplication

import beethoven.instruments  # noqa # pylint: disable=unused-import
from beethoven.ui.apps.piano_trainer import PianoTrainerWidget
from beethoven.ui.main_window import ComposeWidget, MainWindow
from beethoven.ui.components.control import PlayerControlWidget, PlayingType
from beethoven.ui.components.scale_picker import ScalePicker
from beethoven.ui.dialogs import TuningDialog
from beethoven.ui.dialogs.chord_picker import ChordPickerDialog
from beethoven.ui.dialogs.midi import MidiDialog
from beethoven.ui.dialogs.player import PlayerDialog
from beethoven.ui.managers import AppManager
from beethoven.ui.stylesheet import get_stylesheet
from beethoven.ui.utils import get_default_harmony_item


def test_uis():
    print("\n\n")

    qt_application = QApplication([])
    qt_application.setStyleSheet(get_stylesheet())

    manager = AppManager(setting_path=Path(".", "config.ui.json"))

    default_harmony_item = get_default_harmony_item()

    # harmony_items = HarmonyItems.from_list([
    #     {
    #         "scale": "C4_ionian",
    #         "chord_items": [
    #             # {"root": "III", "name": "maj7"},
    #             {"root": "A", "name": ""},
    #             {"root": "D", "name": ""},
    #             # {"root": "E", "name": ""},
    #         ]
    #     },
    # ])

    widget_partials = {
        "tuning": partial(TuningDialog, manager=manager),
        "chord_picker": partial(
            ChordPickerDialog,
            manager=manager,
            current_chord_item=default_harmony_item.chord_items[0],
            current_scale=default_harmony_item.scale,
        ),
        "midi_dialog": partial(
            MidiDialog,
            manager=manager,
        ),
        "player_dialog": partial(
            PlayerDialog,
            manager=manager,
        ),
        "scale_picker": partial(
            ScalePicker,
            current_scale=default_harmony_item.scale,
        ),
        "player_control": partial(
            PlayerControlWidget,
            harmony_items=default_harmony_item,
            playing_type=PlayingType.none,
        ),
        "compose_widget": partial(
            ComposeWidget,
            manager=manager,
        ),
        "piano_trainer_widget": partial(
            PianoTrainerWidget,
            manager=manager,
        ),
        "main_window": partial(
            MainWindow,
            manager=manager,
        ),
    }
    BYPASS = False

    for name, widget_partial in widget_partials.items():
        if BYPASS and name not in ("compose_widget", "main_window"):
            continue

        widget = widget_partial()
        widget.setWindowTitle("Beethoven")
        widget.show()

        qt_application.exec()

    print("\n\n")
