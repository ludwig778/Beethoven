from typing import Optional
from PySide6.QtWidgets import QWidget, QComboBox
from beethoven import controllers

from beethoven.helpers.note import remove_note_octave
from beethoven.models.grid import Grid
from beethoven.models.grid_part import GridPart
from beethoven.models.scale import Scale
from beethoven.ui.components.buttons import Button
from beethoven.ui.components.control import PlayerControlWidget, PlayingType
from beethoven.ui.components.frame import FramedChord, FramedDegree, FramedNotes
from beethoven.ui.components.scale_picker import ScalePicker
from beethoven.ui.constants import C_MAJOR4
from beethoven.ui.layouts import Stretch, horizontal_layout, vertical_layout
from beethoven.ui.managers import AppManager
from PySide6.QtGui import QKeySequence, QShortcut


class HarmonyTrainerWidget(QWidget):
    intervals = {
        "5": 7,
        "4": 5,
        "4a": 6,
        "3": 4,
        "3m": 3,
        "6": 9,
        "6m": 8,
        "2": 2,
        "2m": 1,
        "7": 11,
        "7m": 10,
    }
    notes = controllers.note.parse_list("A,A#,B,C,C#,D,D#,E,F,F#,G,G#")

    def __init__(self, *args, manager: AppManager, **kwargs):
        super(HarmonyTrainerWidget, self).__init__(*args, **kwargs)

        self.manager = manager

        self.current_scale: Optional[Scale] = None

        self.playing_root_frame = FramedNotes()
        self.playing_chord_frame = FramedChord()
        self.playing_degree_frame = FramedDegree()

        self.scale_picker = ScalePicker(
            current_scale=C_MAJOR4
        )

        self.player_widget = PlayerControlWidget(playing_type=PlayingType.step)

        self.reset_button = Button("Reset")
        self.reset_button.pressed.connect(self.reset)

        self.mode_combobox = QComboBox()
        self.mode_combobox.addItems(list(self.intervals.keys()))
        self.mode_combobox.currentTextChanged.connect(self.mode_changed)

        self.action_binding = QShortcut(QKeySequence("Space"), self)
        self.action_binding.activated.connect(self.next)

        self.reset()

        self.setLayout(
            vertical_layout([
                self.scale_picker,
                horizontal_layout([
                    self.mode_combobox,
                    self.reset_button,
                ]),
                horizontal_layout([
                    self.playing_root_frame,
                    self.playing_degree_frame,
                    self.playing_chord_frame,
                ]),
                self.player_widget,
                Stretch(),
            ])
        )

    def reset(self):
        self.current_root = self.scale_picker.get_scale().tonic
        self.current_scale = None

        self.playing_root_frame.set_notes([])

    def next(self):
        if self.current_scale:
            mode_index = self.mode_combobox.currentText()
            mode_offset = self.intervals[mode_index]

            octave = self.scale_picker.get_scale().tonic.octave
            note_index = self.notes.index(remove_note_octave(self.current_root))

            next_index = (note_index + mode_offset) % 12

            current_root = controllers.note.parse(str(self.notes[next_index]) + str(octave))

            self.current_root = current_root
            self.current_scale = controllers.scale.parse(f"{str(current_root)}_{self.current_scale.name}")
        else:
            self.current_scale = self.scale_picker.get_scale()

        self.playing_root_frame.set_notes([self.current_root])
        self.play_current_harmony(continuous=True)

    def mode_changed(self):
        print("mode changed")

    def root_changed(self):
        print("root_changed")

    def play_current_harmony(self, continuous: bool = False):
        if not self.current_scale:
            return

        grid = Grid(
            parts=[
                GridPart(
                    scale=self.current_scale,
                    chord=controllers.chord.parse_with_scale_context("I", scale=self.current_scale),
                    bpm=controllers.bpm.parse("90"),
                    time_signature=controllers.time_signature.parse("4/4"),
                    duration=controllers.duration.parse("160W" if continuous else "1W"),
                )
            ]
        )
        self.manager.play_grid(grid, preview=False)

    def stop(self):
        self.manager.midi.terminate_output_thread()

    def handle_binding_action(self):
        self.harmony_grid.next()

        self.play_current_item(continuous=True)

    def selected_chord_item_changed(self, chord_item):
        self.harmony_grid.update_current_chord(chord_item)

        self.play_current_item()

    def selected_scale_changed(self, scale):
        self.harmony_grid.update_current_scale(scale)

        self.play_current_item()

    def update_harmony(self):
        harmony_item, chord_item = self.harmony_grid.get_current_item()

        self.scale_selector.set_scale(harmony_item.scale)
        self.chord_picker.set_chord_item(chord_item)

    def update_chord(self):
        _, chord_item = self.harmony_grid.get_current_item()

        self.chord_picker.set_chord_item(chord_item)
