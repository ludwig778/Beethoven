from copy import deepcopy
from random import shuffle
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
from beethoven.ui.constants import C_MAJOR4, ROOTS_WITH_SHARPS
from beethoven.ui.layouts import Stretch, horizontal_layout, vertical_layout
from beethoven.ui.managers import AppManager
from PySide6.QtGui import QKeySequence, QShortcut


def note_cycle_generator_factory(interval_semitones):
    def wrapper(start_note):
        note = remove_note_octave(start_note)

        yield start_note

        while 1:
            note_index = ROOTS_WITH_SHARPS.index(note)

            next_note_index = (note_index + interval_semitones) % 12

            note = ROOTS_WITH_SHARPS[next_note_index]

            yield controllers.note.parse(f"{str(note)}{start_note.octave}")

    return wrapper


def random_note_cycle_generator(start_note):
    note = remove_note_octave(start_note)

    notes = deepcopy(ROOTS_WITH_SHARPS)
    notes.remove(note)

    while 1:
        yield start_note

        shuffle(notes)

        for note in notes:
            yield controllers.note.parse(f"{str(note)}{start_note.octave}")


class HarmonyTrainerWidget(QWidget):
    interval_generators = {
        "5": note_cycle_generator_factory(7),
        "4": note_cycle_generator_factory(5),
        "random": random_note_cycle_generator,
        "4a": note_cycle_generator_factory(6),
        "3": note_cycle_generator_factory(4),
        "3m": note_cycle_generator_factory(3),
        "6": note_cycle_generator_factory(9),
        "6m": note_cycle_generator_factory(8),
        "2": note_cycle_generator_factory(2),
        "2m": note_cycle_generator_factory(1),
        "7": note_cycle_generator_factory(11),
        "7m": note_cycle_generator_factory(10),
    }

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
        self.scale_picker.scale_changed.connect(self.reset)

        self.player_widget = PlayerControlWidget(playing_type=PlayingType.step)

        self.reset_button = Button("Reset")
        self.reset_button.pressed.connect(self.reset)

        self.mode_combobox = QComboBox()
        self.mode_combobox.addItems(list(self.interval_generators.keys()))
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
        self.current_root = None
        self.current_scale = None

        self.playing_root_frame.set_notes([])

        mode_index = self.mode_combobox.currentText()

        self.note_generator = self.interval_generators[mode_index](
            self.scale_picker.get_scale().tonic
        )

    def next(self):
        self.current_root = next(self.note_generator)

        if self.current_scale:
            self.current_scale = controllers.scale.parse(f"{str(self.current_root)}_{self.current_scale.name}")
        else:
            self.current_scale = self.scale_picker.get_scale()

        print(self.current_root)
        self.playing_root_frame.set_notes([self.current_root])
        self.play_current_harmony(continuous=True)

    def mode_changed(self):
        print("mode changed")

        self.reset()

    def root_changed(self):
        print("root_changed")

        self.reset()

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
