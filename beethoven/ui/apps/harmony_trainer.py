from copy import deepcopy
from logging import getLogger
from random import shuffle
from typing import Optional, Tuple

from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QComboBox, QLabel, QWidget

from beethoven.models import Chord, Duration, Grid, GridPart, Note, Scale
from beethoven.ui.components.composer_grid import ChordGrid
from beethoven.ui.components.control import PlayerControl
from beethoven.ui.components.frame import (
    FramedChord,
    FramedDegree,
    FramedNotes,
    FramedScale,
)
from beethoven.ui.components.scale_picker import ScalePicker
from beethoven.ui.components.selectors.time_signature import TimeSignatureSelector
from beethoven.ui.components.spinbox import BpmSpinBox
from beethoven.ui.constants import C_MAJOR4, ROOTS_WITH_SHARPS
from beethoven.ui.dialogs.chord_picker import ChordPickerDialog
from beethoven.ui.layouts import Spacing, Stretch, horizontal_layout, vertical_layout
from beethoven.ui.managers import AppManager
from beethoven.ui.models import ChordItem
from beethoven.ui.utils import (
    block_signal,
    connect_push_pull_button_and_dialog,
    get_default_harmony_item,
)

logger = getLogger("trainers.harmony")


def note_cycle_generator_factory(interval_semitones):
    def wrapper(start_note: Note):
        note = start_note.remove_note_octave()

        yield start_note

        while 1:
            note_index = ROOTS_WITH_SHARPS.index(note)

            next_note_index = (note_index + interval_semitones) % 12

            note = ROOTS_WITH_SHARPS[next_note_index]

            yield Note.parse(f"{str(note)}{start_note.octave}")

    return wrapper


def random_note_cycle_generator(start_note: Note):
    note = start_note.remove_note_octave()

    notes = deepcopy(ROOTS_WITH_SHARPS)
    notes.remove(note)

    while 1:
        yield start_note

        shuffle(notes)

        for note in notes:
            yield Note.parse(f"{str(note)}{start_note.octave}")


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

        self.playing_root_frame = FramedNotes(upper_text="Root :")
        self.playing_scale_frame = FramedScale()
        self.playing_chord_frame = FramedChord()
        self.playing_degree_frame = FramedDegree()

        self.scale_selector = ScalePicker(scale=C_MAJOR4)
        self.scale_selector.value_changed.connect(self.reset)

        self.time_signature_selector = TimeSignatureSelector()
        self.bpm_spinbox = BpmSpinBox()

        harmony_item = get_default_harmony_item()

        self.chord_grid = ChordGrid(chord_items=harmony_item.chord_items)
        self.chord_grid.item_changed.connect(self.handle_chord_item_change_from_grid)

        self.chord_picker = ChordPickerDialog(chord_item=harmony_item.chord_items[0])

        connect_push_pull_button_and_dialog(
            self.chord_grid.modify_button, self.chord_picker
        )

        self.chord_picker.value_changed.connect(
            self.handle_chord_item_change_from_picker
        )

        self.player_widget = PlayerControl()

        self.player_widget.play_grid.connect(self.play)
        self.player_widget.stop_grid.connect(self.handle_stop_click)

        self.mode_combobox = QComboBox()
        self.mode_combobox.addItems(list(self.interval_generators.keys()))
        self.mode_combobox.currentTextChanged.connect(self.mode_changed)  # type: ignore

        self.action_binding = QShortcut(QKeySequence("Space"), self)
        self.action_binding.activated.connect(self.next)  # type: ignore

        self.manager.grid_ended.connect(self.play)

        self.reset()

        self.setLayout(
            vertical_layout(
                [
                    horizontal_layout(
                        [
                            Stretch(),
                            QLabel("Harmony step interval:"),
                            Spacing(size=20),
                            self.mode_combobox,
                            Stretch(),
                        ],
                        object_name="step_interval_section",
                    ),
                    Spacing(size=10),
                    horizontal_layout(
                        [
                            Spacing(size=5),
                            self.playing_root_frame,
                            Spacing(size=5),
                            self.playing_degree_frame,
                            Spacing(size=5),
                            self.playing_chord_frame,
                            Spacing(size=5),
                        ]
                    ),
                    Spacing(size=10),
                    horizontal_layout(
                        [
                            vertical_layout(
                                [
                                    QLabel("Scale :"),
                                    QLabel("Time Signature :"),
                                    QLabel("Bpm :"),
                                ],
                                object_name="label_section",
                            ),
                            Stretch(),
                            vertical_layout(
                                [
                                    self.scale_selector,
                                    horizontal_layout(
                                        [self.time_signature_selector, Stretch()]
                                    ),
                                    horizontal_layout([self.bpm_spinbox, Stretch()]),
                                ]
                            ),
                            Spacing(size=5),
                            self.player_widget,
                        ]
                    ),
                    Spacing(size=5),
                    self.chord_grid,
                    Stretch(),
                ],
            )
        )

    def grid_ended(self):
        print("grid_ended")

    def handle_chord_item_change_from_picker(self, chord_item):
        self.chord_grid.update_chord_item(chord_item)

    def handle_chord_item_change_from_grid(self):
        self.chord_picker.set(self.chord_grid.current_item)

    def reset(self):
        self.current_root = None
        self.current_scale = None

        self.playing_root_frame.set_notes([])
        self.playing_root_frame.clear()
        self.playing_chord_frame.clear()
        self.playing_scale_frame.clear()
        self.playing_degree_frame.clear()

        mode_index = self.mode_combobox.currentText()

        self.note_generator = self.interval_generators[mode_index](
            self.scale_selector.value.tonic
        )

    def _on_change(self, grid_part):
        self.current_scale = grid_part.scale

        self.playing_root_frame.set_notes([grid_part.scale.tonic])
        self.playing_chord_frame.set_chord(grid_part.chord)
        self.playing_scale_frame.set_scale(grid_part.scale)
        self.playing_degree_frame.set_degree(grid_part.chord.degree)

    def next(self):
        if self.manager.midi.output_thread:
            with block_signal([self.manager.midi.output_thread]):
                self.manager.midi.terminate_output_thread()

        if self.player_widget.is_key_step_button_pressed():
            self.setup_next_root()
            self.setup_next_scale()

        elif self.player_widget.is_chord_step_button_pressed():
            if not self.current_root:
                self.setup_next_root()
                self.setup_next_scale()
            else:
                self.chord_grid.next()

        self.play()

    def setup_next_root(self):
        self.current_root = next(self.note_generator)

    def setup_next_scale(self):
        if self.current_scale and self.current_root:
            self.current_scale = Scale.build(
                tonic=self.current_root,
                name=self.current_scale.name
            )
        else:
            self.current_scale = self.scale_selector.value

    def play(self):
        if self.player_widget.is_key_step_button_pressed():
            self.play_current_harmony()
        elif self.player_widget.is_chord_step_button_pressed():
            self.play_current_chord()
        elif self.player_widget.is_play_button_pressed():
            self.setup_next_root()
            self.setup_next_scale()

            self.play_current_harmony()

    def mode_changed(self):
        print("mode changed")

        self.reset()

    def root_changed(self):
        print("root_changed")

        self.reset()

    def get_current_chord(self):
        return self.get_chord_from_item(self.chord_grid.current_item)

    def get_current_chords(self):
        return [
            self.get_chord_from_item(chord_item)
            for chord_item in self.chord_grid.get_items()
        ]

    def handle_stop_click(self):
        self.reset()

    def get_chord_from_item(
        self, chord_item: ChordItem
    ) -> Tuple[Chord, Optional[Duration]]:
        chord_name = str(chord_item.root)

        if chord_item.name:
            chord_name += f"_{chord_item.name}"

        return (
            Chord.parse_with_scale_context(
                chord_name, scale=self.current_scale
            ),
            chord_item.duration_item.value,
        )

    def play_current_chord(self):
        current_chord, duration = self.get_current_chord()

        grid = Grid(
            parts=[
                GridPart(
                    scale=self.current_scale,
                    chord=current_chord,
                    bpm=self.bpm_spinbox.value,
                    time_signature=self.time_signature_selector.value,
                    duration=duration,
                )
            ]
        )

        self.manager.play_grid(grid, preview=False, on_grid_part_change=self._on_change)

    def play_current_harmony(self):
        grid = Grid(
            parts=[
                GridPart(
                    scale=self.current_scale,
                    chord=chord,
                    bpm=self.bpm_spinbox.value,
                    time_signature=self.time_signature_selector.value,
                    duration=duration,
                )
                for chord, duration in self.get_current_chords()
            ]
        )

        self.manager.play_grid(grid, preview=False, on_grid_part_change=self._on_change)
