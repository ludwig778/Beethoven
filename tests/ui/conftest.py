from functools import partial

from PySide6.QtWidgets import QApplication
from pytest import fixture

import beethoven.instruments  # noqa # pylint: disable=unused-import
from beethoven.adapters.factory import get_adapters
from beethoven.settings import delete_settings, save_settings, setup_settings
from beethoven.ui.apps.harmony_trainer import HarmonyTrainerWidget
from beethoven.ui.apps.piano_trainer import PianoTrainerWidget
from beethoven.ui.components.scale_picker import ScalePicker
from beethoven.ui.components.sequencer import SequencerWidget
from beethoven.ui.dialogs import TuningDialog
from beethoven.ui.dialogs.chord_picker import ChordPickerDialog
from beethoven.ui.dialogs.midi import MidiDialog
from beethoven.ui.dialogs.player import PlayerDialog
from beethoven.ui.main_window import ComposeWidget, MainWindow
from beethoven.ui.managers import AppManager
from beethoven.ui.stylesheet import get_stylesheet
from beethoven.ui.utils import get_default_harmony_item


@fixture
def qt_application():
    qt_application = QApplication([])
    qt_application.setStyleSheet(get_stylesheet())

    yield qt_application

    del qt_application


@fixture
def manager():
    settings = setup_settings()

    save_settings(settings)

    yield AppManager(settings=settings, adapters=get_adapters())

    delete_settings(settings)


@fixture
def widget_partials(manager):
    default_harmony_item = get_default_harmony_item()

    return {
        "tuning": partial(TuningDialog, manager=manager),
        "chord_picker": partial(
            ChordPickerDialog,
            chord_item=default_harmony_item.chord_items[0],
        ),
        "midi_dialog": partial(MidiDialog, manager=manager),
        "player_dialog": partial(PlayerDialog, manager=manager),
        "scale_picker": partial(ScalePicker, scale=default_harmony_item.scale),
        "sequencer_widget": partial(SequencerWidget, manager=manager),
        "compose_widget": partial(ComposeWidget, manager=manager),
        "piano_trainer_widget": partial(PianoTrainerWidget, manager=manager),
        "harmony_trainer_widget": partial(HarmonyTrainerWidget, manager=manager),
        "main_window": partial(MainWindow, manager=manager),
    }
