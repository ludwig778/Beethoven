from copy import deepcopy
from logging import getLogger
from random import shuffle
from typing import Iterator, List, Tuple

from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QComboBox, QLabel, QWidget

from beethoven.helpers.sequencer import system_tick_logger
from beethoven.models import Degree, Note, Scale
from beethoven.sequencer.runner import SequencerParams
from beethoven.ui.components.composer_grid import ChordGrid
from beethoven.ui.components.frame import HarmonyChordItemFrames
from beethoven.ui.components.scale_picker import ScalePicker
from beethoven.ui.components.selectors.time_signature import TimeSignatureSelector
from beethoven.ui.components.sequencer import SequencerWidget
from beethoven.ui.components.spinbox import BpmSpinBox
from beethoven.ui.constants import C_MAJOR4, ROOTS_WITH_SHARPS
from beethoven.ui.dialogs.chord_picker import ChordPickerDialog
from beethoven.ui.layouts import Spacing, Stretch, horizontal_layout, vertical_layout
from beethoven.ui.managers import AppManager
from beethoven.ui.models import ChordItem, DurationItem, HarmonyItem

logger = getLogger("app.harmony_trainer")


def note_cycle_generator_factory(interval_semitones):
    def wrapper(start_note: Note):
        note = start_note.remove_octave()

        yield start_note

        while 1:
            note_index = ROOTS_WITH_SHARPS.index(note)

            next_note_index = (note_index + interval_semitones) % 12

            note = ROOTS_WITH_SHARPS[next_note_index]

            yield Note.parse(f"{str(note)}{start_note.octave}")

    return wrapper


def random_note_cycle_generator(start_note: Note):
    note = start_note.remove_octave()

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

        self.harmony_chord_frames = HarmonyChordItemFrames()

        self.mode_combobox = QComboBox()
        self.mode_combobox.addItems(list(self.interval_generators.keys()))

        self.scale_selector = ScalePicker(scale=C_MAJOR4)
        self.time_signature_selector = TimeSignatureSelector()
        self.bpm_spinbox = BpmSpinBox()

        self.note_generator: Iterator[Note]
        self.harmony_item: HarmonyItem = HarmonyItem(
            scale=self.scale_selector.value,
            chord_items=[
                ChordItem(
                    root=Degree.parse("I"),
                    name="",
                    duration_item=DurationItem(),
                ),
            ],
            time_signature=self.time_signature_selector.value,
            bpm=self.bpm_spinbox.value,
        )
        self._tonic_array: List[Note]
        self._current_tonic_index: int

        self.setup_note_generator()
        self.setup_root_array()
        self.setup_next_root()

        self.chord_grid = ChordGrid(chord_items=self.harmony_item.chord_items)
        self.chord_picker = ChordPickerDialog(
            chord_item=self.harmony_item.chord_items[0]
        )
        self.sequencer_widget = SequencerWidget(manager=self.manager)

        self.update_frame_display()

        self.mode_combobox.currentTextChanged.connect(self.handle_mode_change)  # type: ignore

        self.chord_grid.item_clicked.connect(self.handle_chord_grid_items_click)
        self.chord_grid.modify_button.connect_to_dialog(self.chord_picker)
        self.chord_grid.item_changed.connect(self.handle_chord_item_change_from_grid)
        self.chord_picker.value_changed.connect(
            self.handle_chord_item_change_from_chord_picker
        )
        self.scale_selector.value_changed.connect(self.handle_scale_change)
        self.time_signature_selector.value_changed.connect(
            self.handle_time_signature_change
        )
        self.bpm_spinbox.value_changed.connect(self.handle_bpm_change)

        self.sequencer_widget.play_button.toggled.connect(
            self.handle_sequencer_widget_play_button
        )
        self.sequencer_widget.key_step_button.toggled.connect(
            self.handle_sequencer_widget_stepper_change
        )
        self.sequencer_widget.chord_step_button.toggled.connect(
            self.handle_sequencer_widget_stepper_change
        )

        self.manager.sequencer.grid_stop.connect(self.reset)

        self.action_binding = QShortcut(QKeySequence("Space"), self)
        self.action_binding.activated.connect(self.handle_action_binding)  # type: ignore

        self.next_binding = QShortcut(QKeySequence("Right"), self)
        self.next_binding.activated.connect(self.handle_next_binding)  # type: ignore

        self.previous_binding = QShortcut(QKeySequence("Left"), self)
        self.previous_binding.activated.connect(self.handle_previous_binding)  # type: ignore

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
                    self.harmony_chord_frames,
                    Spacing(size=5),
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
                            self.sequencer_widget,
                        ]
                    ),
                    Spacing(size=5),
                    self.chord_grid,
                    Stretch(),
                ],
            )
        )

    def setup(self):
        logger.info("setup")

        self.sequencer_widget.setup()

        self.params = self.get_default_params()
        self.manager.sequencer.setup(self.params)

    def teardown(self):
        logger.info("teardown")

        self.sequencer_widget.teardown()

        if not self.manager.sequencer.is_stopped():
            self.manager.sequencer.grid_stop.emit()

    def handle_mode_change(self):
        self.reset()
        self.update_frame_display()

    def setup_note_generator(self):
        mode_index = self.mode_combobox.currentText()

        self.note_generator = self.interval_generators[mode_index](
            self.scale_selector.value.tonic
        )

    def setup_root_array(self):
        self._tonic_array = [
            next(self.note_generator),
        ]
        self._current_tonic_index = -1

    def reset(self):
        self.setup_note_generator()
        self.setup_root_array()
        self.setup_next_root()

        self.chord_grid.set_first_item_as_current_item()

        self.update_frame_display()

    def setup_next_root(self) -> HarmonyItem:
        self._current_tonic_index += 1

        if self._current_tonic_index > len(self._tonic_array) - 2:
            self._tonic_array.append(next(self.note_generator))

        return self.get_harmony_item()

    def setup_previous_root(self) -> HarmonyItem:
        if self._current_tonic_index > 0:
            self._current_tonic_index -= 1

        return self.get_harmony_item()

    def handle_end_grid(self):
        next_harmony = self.setup_next_root()

        self.harmony_item.scale = next_harmony.scale

        self.update_frame_display()

    def get_harmony_item(self, next_item: bool = False):
        index = self._current_tonic_index
        if next_item:
            index += 1

        root = self._tonic_array[index]

        harmony_item = deepcopy(self.harmony_item)
        harmony_item.scale = Scale.build(tonic=root, name=harmony_item.scale.name)

        return harmony_item

    def get_default_params(self) -> SequencerParams:
        def on_item_change(chord_item: ChordItem, harmony_item: HarmonyItem):
            self.chord_grid.set_current_item(chord_item)

        return SequencerParams(
            harmony_items=[self.harmony_item],
            players=self.manager.sequencer.get_players(),
            on_chord_item_change=on_item_change,
            on_tick=system_tick_logger(logger),
        )

    def set_params(self, harmony_items, chord_item, preview: bool = False):
        self.params.update(on_grid_end=None)

        if self.sequencer_widget.is_key_step_button_pressed():
            self.params.set_ranges(selected_harmony_items=harmony_items)
            self.params.set_options(preview=preview)
        elif self.sequencer_widget.is_chord_step_button_pressed():
            self.params.set_ranges(
                selected_harmony_items=harmony_items,
                selected_chord_items=[chord_item],
            )
            self.params.set_options(continuous=True, preview=preview)
        else:
            self.params.clear_ranges()
            self.params.set_options(preview=preview)
            self.params.update(on_grid_end=self.handle_end_grid)

    def handle_chord_grid_items_click(self, chord_item):
        self.set_params(self.harmony_item, chord_item)
        self.params.set_first_items(self.harmony_item, chord_item)

        if self.sequencer_widget.is_play_button_pressed():
            self.manager.sequencer.grid_play.emit()

    def handle_action_binding(self):
        if self.sequencer_widget.is_play_button_pressed():
            if self.sequencer_widget.is_key_step_button_pressed():
                next_harmony_item = self.setup_next_root()
                self.harmony_item.scale = next_harmony_item.scale

                self.chord_grid.set_first_item_as_current_item()

                self.update_frame_display()
            elif self.sequencer_widget.is_chord_step_button_pressed():
                self.chord_grid.next()
            else:
                self.manager.sequencer.grid_stop.emit()

                return

        chord_item = self.chord_grid.current_item

        self.set_params([self.harmony_item], chord_item)
        self.params.set_first_items(self.harmony_item, chord_item)

        self.manager.sequencer.grid_play.emit()

    def handle_next_binding(self):
        if self.sequencer_widget.is_key_step_button_pressed():
            next_harmony_item = self.setup_next_root()
            self.harmony_item.scale = next_harmony_item.scale

            self.chord_grid.set_first_item_as_current_item()

            self.update_frame_display()
        elif self.sequencer_widget.is_chord_step_button_pressed():
            self.chord_grid.next()
        else:
            last_chord_row, current_chord_row = self.chord_grid.next()

            if current_chord_row < last_chord_row:
                next_harmony_item = self.setup_next_root()
                self.harmony_item.scale = next_harmony_item.scale

                self.chord_grid.set_first_item_as_current_item()

                self.update_frame_display()

        chord_item = self.chord_grid.current_item

        self.set_params([self.harmony_item], chord_item)
        self.params.set_first_items(self.harmony_item, chord_item)

        self.manager.sequencer.grid_play.emit()

    def handle_previous_binding(self):
        if self.sequencer_widget.is_key_step_button_pressed():
            next_harmony_item = self.setup_previous_root()
            self.harmony_item.scale = next_harmony_item.scale

            self.update_frame_display()
        elif self.sequencer_widget.is_chord_step_button_pressed():
            self.chord_grid.previous()
        else:
            last_chord_row, current_chord_row = self.chord_grid.previous()

            if last_chord_row == 0:
                next_harmony_item = self.setup_previous_root()
                self.harmony_item.scale = next_harmony_item.scale

                self.chord_grid.set_last_item_as_current_item()

                self.update_frame_display()

        chord_item = self.chord_grid.current_item

        self.set_params([self.harmony_item], chord_item)
        self.params.set_first_items(self.harmony_item, chord_item)

        self.manager.sequencer.grid_play.emit()

    def handle_scale_change(self, scale):
        self.harmony_item.scale = scale

        self.update_frame_display()

    def handle_time_signature_change(self, time_signature):
        self.harmony_item.time_signature = time_signature

    def handle_bpm_change(self, bpm):
        self.params.harmony_items[0].bpm = bpm

    def handle_chord_item_change_from_chord_picker(self, chord_item):
        self.chord_grid.update_chord_item(chord_item)

        self.update_frame_display()

    def handle_chord_item_change_from_grid(self, chord_item: ChordItem):
        self.chord_picker.set(chord_item)

        self.update_frame_display()

    def get_next_items(self) -> Tuple[HarmonyItem, ChordItem]:
        chord_items = self.chord_grid.get_items()
        index = self.chord_grid.current_item.get_index_from(chord_items)
        next_index = index + 1

        if (
            self.sequencer_widget.is_chord_step_button_pressed()
            or self.sequencer_widget.is_key_step_button_pressed()
        ):
            return self.harmony_item, chord_items[next_index % len(chord_items)]

        if next_index >= len(chord_items):
            next_harmony_item = self.get_harmony_item(next_item=True)

            return next_harmony_item, chord_items[0]

        return self.harmony_item, chord_items[next_index]

    def update_frame_display(self):
        self.harmony_chord_frames.update_frames(
            current_items=(self.harmony_item, self.chord_grid.current_item),
            next_items=self.get_next_items(),
        )

    def handle_sequencer_widget_stepper_change(self, state):
        self.set_params([self.harmony_item], self.chord_grid.current_item)
        self.update_frame_display()

    def handle_sequencer_widget_play_button(self, state):
        self.manager.sequencer.grid_play.emit()
