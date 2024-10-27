import logging
from pprint import pprint
from typing import List, TypeVar

from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QWidget

from beethoven.sequencer.instruments import *
# from beethoven.helpers.sequencer import system_tick_logger
from beethoven.models import Bpm, ChordItem, HarmonyItem, Scale, TimeSignature
from beethoven.sequencer.objects import HarmonyItemSelector
from beethoven.ui.components.composer_grid import ComposerGrid
from beethoven.ui.components.display_container import DisplayContainerWidget
from beethoven.ui.components.frame import HarmonyChordItemFrames
from beethoven.ui.components.harmony_picker import HarmonyPicker
from beethoven.ui.components.sequencer import SequencerWidget
from beethoven.ui.dialogs.chord_picker import ChordPickerDialog
from beethoven.ui.layouts import (Spacing, Stretch, horizontal_layout,
                                  vertical_layout)
from beethoven.ui.managers import AppManager
from beethoven.ui.utils import block_signal, get_default_harmony_items

logger = logging.getLogger("app.compose")
# logger.info = print
# logger.debug = print

T = TypeVar("T", HarmonyItem, ChordItem)


class ComposeWidget(QWidget):
    def __init__(
        self,
        *args,
        manager: AppManager,
        harmony_items: List[HarmonyItem] = get_default_harmony_items(),
        **kwargs,
    ):
        super(ComposeWidget, self).__init__(*args, **kwargs)

        self.manager = manager
        self.harmony_items = harmony_items
        self.harmony_iterator = HarmonyItemSelector(self.harmony_items)

        self.harmony_chord_frames = HarmonyChordItemFrames()

        self.composer_grid = ComposerGrid(harmony_iterator=self.harmony_iterator)
        self.composer_grid.items_changed.connect(self.handle_change_from_grid)

        harmony_item, chord_item = self.composer_grid.get_current_items()

        self.display_container = DisplayContainerWidget(
            manager=self.manager,
            harmony_item=harmony_item,
            chord_item=chord_item,
            parent=self,
        )

        self.chord_picker = ChordPickerDialog(
            chord_item=harmony_items[0].chord_items[0], parent=self,
        )
        self.chord_picker.value_changed.connect(self.handle_change_from_chord_picker)
        self.harmony_picker = HarmonyPicker()
        self.harmony_picker.value_changed.connect(self.handle_harmony_change)

        self.sequencer_widget = SequencerWidget(manager=self.manager)

        self.composer_grid.chord_grid.modify_button.connect_to_dialog(self.chord_picker)
        self.composer_grid.chord_grid.setFocus()

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
                    Spacing(size=3),
                    self.harmony_chord_frames,
                    Spacing(size=9),
                    horizontal_layout(
                        [
                            vertical_layout([self.harmony_picker, Stretch()]),
                            Spacing(size=5),
                            self.display_container,
                            Spacing(size=5),
                            vertical_layout([self.sequencer_widget, Stretch()]),
                        ]
                    ),
                    Spacing(size=5),
                    self.composer_grid,
                    Stretch(),
                ],
            )
        )

    def setup(self):
        logger.info("setup")

        self.sequencer_widget.setup()
        self.manager.sequencer_manager.set_harmony_iterator(self.harmony_iterator)

        self.display_container.players_dialog.player_changed.connect(self.reset_players)

        self.manager.sequencer_manager.items_change.connect(self.handle_change_from_sequencer)
        # self.manager.sequencer_manager.sequencer.set_harmony_iterator(self.harmony_iterator)
        self.manager.sequencer_manager.grid_stop.connect(self.reset)

        self.update_frame_display()

    def teardown(self):
        logger.info("teardown")

        self.sequencer_widget.teardown()

        self.display_container.players_dialog.player_changed.disconnect(self.reset_players)

        # self.manager.sequencer_manager.grid_stop.disconnect(self.reset)
        # self.manager.sequencer_manager.items_change.disconnect(self.handle_items_change)

        if not self.manager.sequencer_manager.is_stopped():
            self.manager.sequencer_manager.grid_stop.emit()

    def reset_players(self):
        logger.info("reset players")
        print("reset players" * 22)

        was_running = False
        if not self.manager.sequencer_manager.is_stopped():
            with block_signal([self.manager.sequencer_manager]):
                self.manager.sequencer_manager.grid_stop.emit()

            was_running = True

        if was_running:
            print("RESET PLAYER PLAY()")
            self.play()

    def reset(self):
        logger.info("reset")
        print("reset")

    def play(self, **kwargs):
        kwargs.setdefault("continuous", self.sequencer_widget.is_chord_step_button_pressed())
        kwargs.setdefault("preview", self.manager.sequencer_manager.is_playing_preview())

        print("PLAY")
        pprint(kwargs)
        self.manager.sequencer_manager.play(**kwargs)

    def stop(self, **kwargs):
        self.manager.sequencer_manager.stop(**kwargs)

    def handle_items_change(
        self,
        harmony_item: HarmonyItem,
        chord_item: ChordItem,
        from_composer_grid: bool = False,
        from_chord_picker: bool = False,
        from_harmony_picker: bool = False,
    ):
        # print("=" * 66)
        # print("ComposeWidget::handle_items_change", bool(from_composer_grid), bool(from_chord_picker), bool(from_harmony_picker), bool(from_sequencer))
        # print(f"{harmony_item.scale.to_log_string()} = {chord_item.to_simple_string()}")
        # print()

        if not from_composer_grid:
            with block_signal([self.composer_grid]):
                self.composer_grid.set_current_items(harmony_item, chord_item)
        if not from_chord_picker:
            with block_signal([self.chord_picker]):
                self.chord_picker.set(chord_item)
        if not from_harmony_picker:
            with block_signal([self.harmony_picker]):
                self.harmony_picker.set(harmony_item)

        self.display_container.update_items(harmony_item, chord_item)

        self.update_frame_display()

        # if not from_sequencer:
        #     self.play()

    def handle_action_binding(self):
        print()
        print("KEY   : ", self.sequencer_widget.is_key_step_button_pressed())
        print("CHORD : ", self.sequencer_widget.is_chord_step_button_pressed())
        print()
        if self.sequencer_widget.is_play_button_pressed():
            if (
                self.sequencer_widget.is_key_step_button_pressed()
                or self.sequencer_widget.is_chord_step_button_pressed()
            ):
                next_items = self.harmony_iterator.next()

                logger.info(f"hid={next_items[0].id} cid={next_items[1].id}")

                print("ComposeWidget::handle_action_binding 0")
                self.play()
            else:
                print("ComposeWidget::handle_action_binding 1")
                self.stop()
        else:
            print("ComposeWidget::handle_action_binding 2")

            self.play()

    def handle_next_binding(self):
        next_items = self.harmony_iterator.next()

        logger.info(f"hid={next_items[0].id} cid={next_items[1].id}")

        self.handle_items_change(*next_items)

        # if self.sequencer_widget.is_play_button_pressed():
        print("NEXT BINDING PLAY()")
        if self.manager.sequencer_manager.is_stopped() or self.manager.sequencer_manager.is_playing_preview():
            self.play(preview=True)
        else:
            self.play()

    def handle_previous_binding(self):
        previous_items = self.harmony_iterator.previous()

        logger.info(f"hid={previous_items[0].id} cid={previous_items[1].id}")

        self.handle_items_change(*previous_items)

        # if self.manager.sequencer_manager.is_playing():
        print("PREVIOUS BINDING PLAY()")
        if self.manager.sequencer_manager.is_stopped() or self.manager.sequencer_manager.is_playing_preview():
            self.play(preview=True)
        else:
            self.play()

    def handle_change_from_grid(self, harmony_item: HarmonyItem, chord_item: ChordItem, harmony_change: bool):
        logger.info(f"hid={harmony_item.id} cid={chord_item.id} {harmony_change=}")
        # print(f"hid={harmony_item.id} cid={chord_item.id} {harmony_change=}")

        self.handle_items_change(harmony_item, chord_item, from_composer_grid=True)

        with block_signal([self.composer_grid]):
            self.composer_grid.set_current_items(harmony_item, chord_item)

        print("GRID CHANGE PLAY()")
        if not harmony_change:
            if self.manager.sequencer_manager.is_stopped() or self.manager.sequencer_manager.is_playing_preview():
                self.play(preview=True)
            else:
                self.play()

    def handle_change_from_chord_picker(self, chord_item):
        logger.info(f"chord item={chord_item.to_log_string()}")

        self.handle_items_change(self.harmony_iterator.current_harmony_item, chord_item, from_chord_picker=True)

        print("CHORD PICKER CHANGE PLAY()")
        if self.manager.sequencer_manager.is_stopped() or self.manager.sequencer_manager.is_playing_preview():
            self.play(preview=True)
        else:
            self.play()

    def handle_sequencer_stepper_change(self, _):
        key_step = self.sequencer_widget.is_key_step_button_pressed()
        chord_step = self.sequencer_widget.is_chord_step_button_pressed()

        logger.info(f"set {key_step=} {chord_step=}")

        self.harmony_iterator.set_chord_looping(key_step)

        self.handle_items_change(*self.harmony_iterator.current_items)

    def handle_change_from_sequencer(self, harmony_item: HarmonyItem, chord_item: ChordItem):
        self.handle_items_change(harmony_item, chord_item)

    def handle_harmony_change(
        self,
        scale: Scale | None,
        time_signature: TimeSignature | None,
        bpm: Bpm | None,
    ):
        print("ComposeWidget::handle_harmony_change")
        logger.info(
            f"scale={scale.to_log_string() if scale else 'None'} "
            f"time_signature={str(time_signature)} bpm={str(bpm)}"
        )

        if time_signature:
            self.harmony_iterator.current_harmony_item.time_signature = time_signature
            self.composer_grid.harmony_grid.refresh_current_index()

        if bpm:
            self.harmony_iterator.current_harmony_item.bpm = bpm
            self.composer_grid.harmony_grid.refresh_current_index()

        if scale:
            self.harmony_iterator.current_harmony_item.scale = scale
            self.composer_grid.harmony_grid.refresh_current_index()

            self.display_container.update_items(*self.harmony_iterator.current_items)

        if scale or time_signature:
            if self.manager.sequencer_manager.is_playing():
                self.play(if_playing=True)
            else:
                self.update_frame_display()

    def update_frame_display(self):
        self.harmony_chord_frames.update_frames(
            current_items=self.harmony_iterator.current_items,
            next_items=self.harmony_iterator.get_next_items()[0],
        )
