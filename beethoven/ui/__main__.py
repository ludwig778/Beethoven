import atexit
from enum import Enum, auto
from pathlib import Path
from logging import getLogger
from beethoven import controllers
from beethoven.helpers.note import remove_note_octave
from beethoven.models.grid import Grid
from beethoven.models.grid_part import GridPart
from beethoven.models.scale import Scale
from beethoven.ui.components.buttons import Button, PushPullButton
from beethoven.ui.components.chord_picker import ChordPicker
from beethoven.ui.components.combobox import NoteComboBox, ScaleComboBox
from beethoven.ui.components.harmony_grid import HarmonyGrid
from beethoven.ui.layouts import horizontal_layout, vertical_layout
from beethoven.ui.managers import AppManager
from beethoven.ui.models import HarmonyItems
from beethoven.ui.stylesheet import get_stylesheet
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QSpinBox, QWidget, QApplication

from beethoven.ui.utils import block_signal

logger = getLogger("ui.main")


class ScaleSelector(QWidget):
    scale_changed = Signal(Scale)

    def __init__(self, *args, current_scale: Scale, **kwargs):
        super(ScaleSelector, self).__init__(*args, **kwargs)

        self.root_combobox = NoteComboBox(
            selected_note=remove_note_octave(current_scale.tonic)
        )
        self.name_combobox = ScaleComboBox(selected_scale_name=current_scale.name)
        self.octave_spinbox = QSpinBox()
        self.octave_spinbox.setMinimum(0)
        self.octave_spinbox.setMaximum(10)
        self.octave_spinbox.setValue(current_scale.tonic.octave or 4)

        self.root_combobox.note_changed.connect(self.update_scale)
        self.name_combobox.scale_name_changed.connect(self.update_scale)
        self.octave_spinbox.valueChanged.connect(self.update_scale)

        self.setLayout(
            horizontal_layout([
                self.root_combobox,
                self.name_combobox,
                self.octave_spinbox,
            ])
        )

    def set_scale(self, scale):
        self.root_combobox.set_note(scale.tonic)
        self.name_combobox.set_scale_name(scale.name)
        self.octave_spinbox.setValue(scale.tonic.octave or 4)

    def get_scale(self):
        tonic = self.root_combobox.get_note()
        scale_name = self.name_combobox.get_scale_name()
        octave = self.octave_spinbox.value()

        return controllers.scale.parse(f"{tonic}{octave}_{scale_name}")

    def update_scale(self, *args):
        self.scale_changed.emit(self.get_scale())


class PlayingType(Enum):
    NONE = auto()
    STEP = auto()


class PlayerWidget(QWidget):
    play_grid = Signal()
    play_grid_step = Signal()
    stop_grid = Signal()

    def __init__(
        self, *args, harmony_items: HarmonyItems, playing_type: PlayingType, **kwargs
    ):
        super(PlayerWidget, self).__init__(*args, **kwargs)

        self.harmony_items = harmony_items

        self.step_player_button = PushPullButton(
            pressed="Step", released="Step", state=playing_type == PlayingType.STEP
        )
        self.play_button = PushPullButton(pressed="Play", released="Play", state=False)
        self.stop_button = Button("Stop")

        self.step_player_button.toggled.connect(self.step_play)
        self.play_button.toggled.connect(self.play)
        self.stop_button.clicked.connect(self.clear)

        self.setLayout(
            horizontal_layout([
                self.step_player_button,
                self.play_button,
                self.stop_button,
            ])
        )

    def step_play(self, state):
        print("STEP PLAY", state)
        if self.play_button.is_pressed:
            with block_signal([self.play_button]):
                self.play_button.release()

            self.stop_grid.emit()

        if state:
            self.play_grid_step.emit()

    def play(self, state):
        print("PLAY", state)
        if self.step_player_button.is_pressed:
            with block_signal([self.step_player_button]):
                self.step_player_button.release()

            self.stop_grid.emit()

        if state:
            self.play_grid.emit()

    def clear(self):
        with block_signal([self.step_player_button, self.play_button]):
            self.step_player_button.release()
            self.play_button.release()

        self.stop_grid.emit()


class App(QWidget):
    def __init__(
        self, *args, manager: AppManager, harmony_items: HarmonyItems, **kwargs
    ):
        super(App, self).__init__(*args, **kwargs)

        self.setWindowTitle("qt.py")

        self.manager = manager

        self.harmony_grid = HarmonyGrid(manager=manager, harmony_items=harmony_items)
        self.harmony_grid.harmony_item_changed.connect(self.update_harmony)
        self.harmony_grid.chord_item_changed.connect(self.update_chord)

        harmony_item, chord_item = self.harmony_grid.get_current_item()

        self.player_widget = PlayerWidget(
            harmony_items=harmony_items, playing_type=PlayingType.STEP
        )

        self.chord_picker = ChordPicker(
            manager=manager,
            current_chord_item=chord_item,
            current_scale=harmony_item.scale,
        )
        self.scale_selector = ScaleSelector(current_scale=harmony_item.scale)

        self.chord_picker.chord_item_changed.connect(self.selected_chord_item_changed)
        self.scale_selector.scale_changed.connect(self.selected_scale_changed)

        self.player_widget.play_grid_step.connect(self.play_current_item)
        self.player_widget.stop_grid.connect(self.stop)

        self.action_binding = QShortcut(QKeySequence("Space"), self)
        self.action_binding.activated.connect(self.handle_binding_action)

        self.setLayout(
            vertical_layout([
                self.chord_picker,
                horizontal_layout([
                    self.scale_selector,
                    self.player_widget,
                ]),
                self.harmony_grid,
            ])
        )

    def play_current_item(self):
        harmony_item, chord_item = self.harmony_grid.get_current_item()

        grid = Grid(
            parts=[
                GridPart(
                    scale=harmony_item.scale,
                    chord=chord_item.as_chord(scale=harmony_item.scale),
                    bpm=controllers.bpm.parse("90"),
                    time_signature=controllers.time_signature.parse("4/4"),
                    duration=controllers.duration.parse("4W"),
                )
            ],
        )
        self.manager.play_grid(grid, preview=True)

    def stop(self):
        self.manager.midi.terminate_output_thread()

    def handle_binding_action(self):
        self.harmony_grid.next()

        self.play_current_item()

    def selected_chord_item_changed(self, chord_item):
        self.harmony_grid.update_current_chord(chord_item)

    def selected_scale_changed(self, scale):
        self.harmony_grid.update_current_scale(scale)

    def update_harmony(self):
        harmony_item, chord_item = self.harmony_grid.get_current_item()

        self.scale_selector.set_scale(harmony_item.scale)
        self.chord_picker.set_chord_item(chord_item)

    def update_chord(self):
        _, chord_item = self.harmony_grid.get_current_item()

        self.chord_picker.set_chord_item(chord_item)


def main():
    app = QApplication([])
    app.setStyleSheet(get_stylesheet())

    setting_path = Path(".", "config.ui.json")
    manager = AppManager(setting_path=setting_path)

    harmony_items = HarmonyItems.from_list(
        [
            {
                "scale": "C4_ionian",
                "chord_items": [
                    # {"root": "III", "name": "maj7"},
                    {"root": "A", "name": ""},
                    {"root": "D", "name": ""},
                    # {"root": "E", "name": ""},
                ],
            },
        ]
    )
    atexit.register(manager.midi.terminate_threads)
    window = App(manager=manager, harmony_items=harmony_items)
    window.setWindowTitle("Beethoven")

    # set_size_policies([w], QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
