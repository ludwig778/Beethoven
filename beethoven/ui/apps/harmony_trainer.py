import logging
from copy import deepcopy
from dataclasses import replace
from random import shuffle
from typing import List, Optional, Tuple, TypeVar

from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QComboBox, QLabel, QWidget

from beethoven.helpers.sequencer import system_tick_logger
from beethoven.models import Bpm, ChordItem, HarmonyItem, Note, Scale, TimeSignature
from beethoven.sequencer.runner import SequencerItemIterator, SequencerParams
from beethoven.types import SequencerItems
from beethoven.ui.components.composer_grid import ChordGrid
from beethoven.ui.components.frame import HarmonyChordItemFrames
from beethoven.ui.components.harmony_picker import HarmonyPicker
from beethoven.ui.components.sequencer import SequencerWidget
from beethoven.ui.constants import ROOTS_WITH_SHARPS
from beethoven.ui.dialogs.chord_picker import ChordPickerDialog
from beethoven.ui.layouts import Spacing, Stretch, horizontal_layout, vertical_layout
from beethoven.ui.managers import AppManager
from beethoven.ui.utils import get_default_harmony_item

logger = logging.getLogger("app.harmony_trainer")

T = TypeVar("T", HarmonyItem, ChordItem)


def note_cycle_generator_factory(interval_semitones: int):
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


class HarmonyItemGenerator:
    generators = {
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

    def __init__(self, harmony_item, generator_name: str = "5"):
        self.original_item = harmony_item
        self.current_item = harmony_item

        self.setup(harmony_item.scale, generator_name)

    def set_bpm(self, bpm: Bpm):
        self.current_item.bpm = bpm
        self.next_item.bpm = bpm

        self.original_item = replace(self.original_item, bpm=bpm)

    def set_time_signature(self, time_signature: TimeSignature):
        self.current_item.time_signature = time_signature
        self.next_item.time_signature = time_signature

        self.original_item = replace(self.original_item, time_signature=time_signature)

    def setup(self, scale: Optional[Scale] = None, generator_name: Optional[str] = None):
        if scale:
            self.original_item = replace(self.original_item, scale=scale)
            self.current_item = self.original_item
        if generator_name:
            self.generator_name = generator_name

        self.generator = self.generators[self.generator_name](self.current_item.scale.tonic)

        current_tonic = next(self.generator)

        next_tonic = next(self.generator)
        self.next_item = replace(
            self.current_item, scale=replace(self.original_item.scale, tonic=next_tonic)
        )

        self._index = 0
        self._tonics = [current_tonic, next_tonic]

    def next(self) -> Tuple[HarmonyItem, HarmonyItem]:
        self._index += 1
        if self._index > len(self._tonics) - 2:
            self._tonics.append(next(self.generator))

        self.current_item = replace(
            self.original_item,
            scale=replace(self.original_item.scale, tonic=self._tonics[self._index]),
        )
        self.next_item = replace(
            self.original_item,
            scale=replace(self.original_item.scale, tonic=self._tonics[self._index + 1]),
        )

        return self.current_item, self.next_item

    def previous(self) -> Tuple[HarmonyItem, HarmonyItem]:
        if self._index > 0:
            self._index -= 1

        self.current_item = replace(
            self.original_item,
            scale=replace(self.original_item.scale, tonic=self._tonics[self._index]),
        )
        self.next_item = replace(
            self.original_item,
            scale=replace(self.original_item.scale, tonic=self._tonics[self._index + 1]),
        )

        return self.current_item, self.next_item


class HarmonyTrainerWidget(QWidget):
    def __init__(self, *args, manager: AppManager, **kwargs):
        super(HarmonyTrainerWidget, self).__init__(*args, **kwargs)

        self.manager = manager

        self.harmony_chord_frames = HarmonyChordItemFrames()

        self.mode_combobox = QComboBox()
        self.mode_combobox.addItems(list(HarmonyItemGenerator.generators.keys()))
        self.mode_combobox.setObjectName("mode_combobox")

        self.harmony_item_generator = HarmonyItemGenerator(get_default_harmony_item())

        self.chord_grid = ChordGrid(chord_items=self.harmony_item_generator.current_item.chord_items)
        self.chord_picker = ChordPickerDialog(
            chord_item=self.harmony_item_generator.current_item.chord_items[0]
        )
        self.harmony_picker = HarmonyPicker()

        self.sequencer_widget = SequencerWidget(manager=self.manager)

        self.mode_combobox.currentTextChanged.connect(self.handle_mode_change)  # type: ignore

        self.chord_grid.item_added.connect(self.handle_added_chord_item)
        self.chord_grid.item_clicked.connect(self.handle_click_from_grid)
        self.chord_grid.modify_button.connect_to_dialog(self.chord_picker)
        self.chord_grid.item_deleted.connect(self.handle_deleted_chord_item)

        self.chord_picker.value_changed.connect(self.handle_change_from_chord_picker)
        self.harmony_picker.value_changed.connect(self.handle_harmony_change)

        self.sequencer_widget.key_step_button.toggled.connect(self.handle_sequencer_stepper_change)
        self.sequencer_widget.chord_step_button.toggled.connect(self.handle_sequencer_stepper_change)

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
                    Spacing(size=1),
                    self.harmony_chord_frames,
                    Spacing(size=1),
                    horizontal_layout(
                        [
                            vertical_layout([self.harmony_picker, Stretch()]),
                            Spacing(size=5),
                            vertical_layout([self.sequencer_widget, Stretch()]),
                        ]
                    ),
                    Spacing(size=5),
                    self.chord_grid,
                    Stretch(),
                ]
            )
        )

    def setup(self):
        logger.info("setup")

        self.sequencer_widget.setup()
        self.sequencer_iterator = SequencerItemIterator.setup(
            current_items=(
                self.harmony_item_generator.current_item,
                self.harmony_item_generator.current_item.chord_items[0],
            ),
            next_items_updater=self.next_items_update,
        )
        self.params = SequencerParams(
            item_iterator=self.sequencer_iterator,
            players=self.manager.sequencer.get_players(),
            on_chord_item_change=self.manager.sequencer.items_change.emit,
            on_tick=system_tick_logger(logger, level=logging.DEBUG),
            on_grid_end=self.manager.sequencer.grid_ended.emit,
        )

        self.manager.sequencer.items_change.connect(self.handle_items_change)
        self.manager.sequencer.setup(self.params)
        self.manager.sequencer.grid_stop.connect(self.reset)

        self.update_frame_display()

    def teardown(self):
        logger.info("teardown")

        self.sequencer_widget.teardown()

        self.manager.sequencer.grid_stop.disconnect(self.reset)
        self.manager.sequencer.items_change.disconnect(self.handle_items_change)

        if not self.manager.sequencer.is_stopped():
            self.manager.sequencer.grid_stop.emit()

    def reset(self):
        logger.info("reset")

        self.params.set_options(preview=False)

        self.harmony_item_generator.setup(scale=self.harmony_picker.scale)

        harmony_item = self.harmony_item_generator.current_item

        self.sequencer_iterator.reset((harmony_item, harmony_item.chord_items[0]))

        self.handle_items_change(*self.sequencer_iterator.current_items)

    def _get_next_item(self, items: List[T], current_item: T) -> Tuple[T, bool]:
        next_index = items.index(current_item) + 1
        next_item = items[next_index % len(items)]

        return next_item, next_index >= len(items)

    def _get_previous_item(self, items: List[T], current_item: T) -> Tuple[T, bool]:
        previous_index = items.index(current_item) - 1
        previous_item = items[previous_index % len(items)]

        return previous_item, previous_index < 0

    def get_next_items(self, harmony_item: HarmonyItem, chord_item: ChordItem) -> SequencerItems:
        next_harmony_item = harmony_item
        next_chord_item = chord_item

        if self.sequencer_widget.is_key_step_button_pressed():
            next_harmony_item = self.harmony_item_generator.next_item
            next_chord_item = next_harmony_item.chord_items[0]
        elif self.sequencer_widget.is_chord_step_button_pressed():
            next_chord_item, _ = self._get_next_item(harmony_item.chord_items, chord_item)
        else:
            next_chord_item, chord_reset = self._get_next_item(harmony_item.chord_items, chord_item)

            if chord_reset:
                next_harmony_item = self.harmony_item_generator.current_item

        return next_harmony_item, next_chord_item

    def get_previous_items(self, harmony_item: HarmonyItem, chord_item: ChordItem) -> SequencerItems:
        previous_harmony_item = harmony_item
        previous_chord_item = chord_item

        if self.sequencer_widget.is_key_step_button_pressed():
            previous_harmony_item, _ = self.harmony_item_generator.previous()
        elif self.sequencer_widget.is_chord_step_button_pressed():
            previous_chord_item, _ = self._get_previous_item(harmony_item.chord_items, chord_item)
        else:
            previous_chord_item, chord_reset = self._get_previous_item(
                harmony_item.chord_items, chord_item
            )

            if chord_reset:
                previous_harmony_item, _ = self.harmony_item_generator.previous()
                previous_chord_item = previous_harmony_item.chord_items[-1]
            else:
                previous_harmony_item = harmony_item

        return previous_harmony_item, previous_chord_item

    def next_items_update(self, harmony_item: HarmonyItem, chord_item: ChordItem) -> SequencerItems:
        next_harmony_item = harmony_item
        next_chord_item = chord_item

        if self.sequencer_widget.is_key_step_button_pressed():
            next_chord_item, _ = self._get_next_item(harmony_item.chord_items, chord_item)
        elif not self.sequencer_widget.is_chord_step_button_pressed():
            next_chord_item, chord_reset = self._get_next_item(harmony_item.chord_items, chord_item)

            if chord_reset:
                next_harmony_item, _ = self.harmony_item_generator.next()

        return next_harmony_item, next_chord_item

    def handle_items_change(self, harmony_item: HarmonyItem, chord_item: ChordItem):
        logger.info(f"hid={harmony_item.id} cid={chord_item.id}")

        self.chord_grid.set_current_item(chord_item)

        self.chord_picker.set(chord_item)

        self.update_frame_display()

    def handle_action_binding(self):
        if self.sequencer_widget.is_play_button_pressed():
            if (
                self.sequencer_widget.is_key_step_button_pressed()
                or self.sequencer_widget.is_chord_step_button_pressed()
            ):
                next_items = self.get_next_items(*self.sequencer_iterator.current_items)

                logger.info(f"hid={next_items[0].id} cid={next_items[1].id}")

                self.sequencer_iterator.reset(next_items)
                self.manager.sequencer.grid_play.emit()
            else:
                self.manager.sequencer.grid_stop.emit()

                return
        else:
            current_items = self.sequencer_iterator.current_items

            logger.info(f"hid={current_items[0].id} cid={current_items[1].id}")

            self.manager.sequencer.grid_play.emit()

    def handle_next_binding(self):
        next_items = self.get_next_items(*self.sequencer_iterator.current_items)

        self.sequencer_iterator.reset(next_items)

        logger.info(f"hid={next_items[0].id} cid={next_items[1].id}")

        if self.sequencer_widget.is_play_button_pressed():
            self.manager.sequencer.grid_play.emit()
        else:
            self.handle_items_change(*self.sequencer_iterator.current_items)

    def handle_previous_binding(self):
        previous_items = self.get_previous_items(*self.sequencer_iterator.current_items)

        self.sequencer_iterator.reset(previous_items)

        logger.info(f"hid={previous_items[0].id} cid={previous_items[1].id}")

        if self.sequencer_widget.is_play_button_pressed():
            self.manager.sequencer.grid_play.emit()
        else:
            self.handle_items_change(*self.sequencer_iterator.current_items)

    def handle_click_from_grid(self, chord_item):
        logger.info(f"cid={chord_item.id}")

        self.sequencer_iterator.reset((self.harmony_item_generator.current_item, chord_item))

        self.update_frame_display()

        if self.manager.sequencer.is_playing():
            self.manager.sequencer.grid_play.emit()
        else:
            self.handle_items_change(*self.sequencer_iterator.current_items)

    def handle_change_from_chord_picker(self, chord_item):
        logger.info(f"chord item={chord_item.to_log_string()}")

        self.chord_grid.update_chord_item(chord_item)

        if self.manager.sequencer.is_playing_preview() or self.manager.sequencer.is_stopped():
            self.params.set_options(preview=True)

        self.manager.sequencer.grid_play.emit()

    def handle_sequencer_stepper_change(self, _):
        continuous = self.sequencer_widget.is_chord_step_button_pressed()

        logger.info(f"set {continuous=}")

        self.sequencer_iterator.reset(self.sequencer_iterator.current_items)

        self.params.set_options(continuous=continuous)

        self.handle_items_change(*self.sequencer_iterator.current_items)

    def _set_current_chord_item(self, chord_item: ChordItem):
        harmony_item = self.harmony_item_generator.current_item

        self.sequencer_iterator.reset((harmony_item, chord_item))

        if self.sequencer_widget.is_play_button_pressed():
            self.manager.sequencer.grid_play.emit()
        else:
            self.update_frame_display()

    def handle_added_chord_item(self, chord_item: ChordItem):
        logger.info(f"{chord_item.to_log_string()}")

        self._set_current_chord_item(chord_item)

    def handle_deleted_chord_item(self, _: ChordItem, chord_item: ChordItem):
        logger.info(f"setting as current item cid={chord_item.id}")

        self._set_current_chord_item(chord_item)

    def handle_mode_change(self, mode: str):
        logger.info(f"setting mode={mode}")

        self.harmony_item_generator.setup(
            scale=self.sequencer_iterator.current_items[0].scale, generator_name=mode
        )

        self.sequencer_iterator.reset(self.sequencer_iterator.current_items)

        self.update_frame_display()

    def handle_harmony_change(
        self,
        scale: Optional[Scale],
        time_signature: Optional[TimeSignature],
        bpm: Optional[Bpm],
    ):
        logger.info(
            f"scale={scale.to_log_string() if scale else 'None'} "
            f"time_signature={str(time_signature)} bpm={str(bpm)}"
        )

        if time_signature:
            self.harmony_item_generator.set_time_signature(time_signature)

        if bpm:
            self.harmony_item_generator.set_bpm(bpm)

        if scale:
            self.harmony_item_generator.setup(scale)

            self.sequencer_iterator.reset(
                (
                    self.harmony_item_generator.current_item,
                    self.sequencer_iterator.current_items[1],
                )
            )

        if scale or time_signature:
            if self.manager.sequencer.is_playing():
                self.manager.sequencer.grid_play.emit()
            else:
                self.update_frame_display()

    def update_frame_display(self):
        if self.sequencer_widget.is_chord_step_button_pressed():
            self.harmony_chord_frames.update_frames(
                current_items=self.sequencer_iterator.current_items,
                next_items=self.get_next_items(*self.sequencer_iterator.current_items),
            )
        else:
            self.harmony_chord_frames.update_frames(
                current_items=self.sequencer_iterator.current_items,
                next_items=self.sequencer_iterator.next_items,
            )
