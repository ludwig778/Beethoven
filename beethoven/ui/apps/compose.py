from logging import getLogger
from typing import List, Tuple

from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QLabel, QWidget

from beethoven.helpers.sequencer import system_tick_logger
from beethoven.sequencer.runner import SequencerParams
from beethoven.ui.components.composer_grid import ComposerGrid
from beethoven.ui.components.frame import HarmonyChordItemFrames
from beethoven.ui.components.scale_picker import ScalePicker
from beethoven.ui.components.selectors.time_signature import TimeSignatureSelector
from beethoven.ui.components.sequencer import SequencerWidget
from beethoven.ui.components.spinbox import BpmSpinBox
from beethoven.ui.dialogs.chord_picker import ChordPickerDialog
from beethoven.ui.layouts import Spacing, Stretch, horizontal_layout, vertical_layout
from beethoven.ui.managers import AppManager
from beethoven.ui.models import ChordItem, HarmonyItem
from beethoven.ui.utils import get_default_harmony_items

logger = getLogger("app.compose")


class ComposeWidget(QWidget):
    def __init__(
        self,
        *args,
        manager: AppManager,
        harmony_items: List[HarmonyItem] = get_default_harmony_items(),
        **kwargs
    ):
        super(ComposeWidget, self).__init__(*args, **kwargs)

        self.manager = manager

        self.harmony_chord_frames = HarmonyChordItemFrames()

        self.composer_grid = ComposerGrid(harmony_items=harmony_items)
        self.composer_grid.harmony_item_changed.connect(
            self.handle_harmony_item_change_from_grid
        )
        self.composer_grid.chord_item_changed.connect(
            self.handle_chord_item_change_from_grid
        )

        harmony_item, chord_item = self.composer_grid.get_current_items()

        self.scale_selector = ScalePicker(scale=harmony_item.scale)
        self.time_signature_selector = TimeSignatureSelector()
        self.bpm_spinbox = BpmSpinBox()
        self.sequencer_widget = SequencerWidget(manager=self.manager)
        self.chord_picker = ChordPickerDialog(chord_item=chord_item, parent=self)

        self.update_frame_display()

        self.composer_grid.item_clicked.connect(self.handle_composer_grid_items_click)

        self.composer_grid.chord_grid.modify_button.connect_to_dialog(self.chord_picker)
        self.scale_selector.octave_spinbox.clearFocus()
        self.composer_grid.chord_grid.setFocus()

        self.scale_selector.value_changed.connect(self.handle_scale_change)
        self.time_signature_selector.value_changed.connect(
            self.handle_time_signature_change
        )
        self.bpm_spinbox.value_changed.connect(self.handle_bpm_change)
        self.chord_picker.value_changed.connect(
            self.handle_chord_item_change_from_chord_picker
        )

        self.sequencer_widget.play_button.toggled.connect(
            self.handle_sequencer_widget_play_button
        )
        self.sequencer_widget.key_step_button.toggled.connect(
            self.handle_sequencer_widget_stepper_change
        )
        self.sequencer_widget.chord_step_button.toggled.connect(
            self.handle_sequencer_widget_stepper_change
        )

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
                    self.composer_grid,
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

    def get_default_params(self) -> SequencerParams:
        def on_item_change(chord_item: ChordItem, harmony_item: HarmonyItem):
            self.composer_grid.set_current_items(
                harmony_item=harmony_item, chord_item=chord_item
            )

        params = SequencerParams(
            players=self.manager.sequencer.get_players(),
            on_chord_item_change=on_item_change,
            on_tick=system_tick_logger(logger),
            on_grid_end=self.manager.sequencer.grid_ended.emit,
        )

        # TODO: Check if changed, pydantic does not pass list reference
        # using Config.copy_on_model_validation already tried
        params.harmony_items = self.composer_grid.harmony_items

        return params

    def handle_composer_grid_items_click(self, harmony_item, chord_item):
        self.set_params(harmony_item, chord_item)
        self.params.set_first_items(harmony_item, chord_item)

        if self.sequencer_widget.is_play_button_pressed():
            self.manager.sequencer.grid_play.emit()

    def handle_action_binding(self):
        if self.sequencer_widget.is_play_button_pressed():
            if self.sequencer_widget.is_key_step_button_pressed():
                self.composer_grid.harmony_grid.next()
            elif self.sequencer_widget.is_chord_step_button_pressed():
                self.composer_grid.chord_grid.next()
            else:
                self.manager.sequencer.grid_stop.emit()

                return

        harmony_item, chord_item = self.composer_grid.get_current_items()

        self.set_params(harmony_item, chord_item)
        self.params.set_first_items(harmony_item, chord_item)

        self.manager.sequencer.grid_play.emit()

    def handle_next_binding(self):
        if self.sequencer_widget.is_key_step_button_pressed():
            self.composer_grid.harmony_grid.next()
        elif self.sequencer_widget.is_chord_step_button_pressed():
            self.composer_grid.chord_grid.next()
        else:
            self.composer_grid.next()

        harmony_item, chord_item = self.composer_grid.get_current_items()

        self.set_params(harmony_item, chord_item)
        self.params.set_first_items(harmony_item, chord_item)

        self.manager.sequencer.grid_play.emit()

    def handle_previous_binding(self):
        if self.sequencer_widget.is_key_step_button_pressed():
            self.composer_grid.harmony_grid.previous()
        elif self.sequencer_widget.is_chord_step_button_pressed():
            self.composer_grid.chord_grid.previous()
        else:
            self.composer_grid.previous()

        harmony_item, chord_item = self.composer_grid.get_current_items()

        self.set_params(harmony_item, chord_item)
        self.params.set_first_items(harmony_item, chord_item)

        self.manager.sequencer.grid_play.emit()

    def set_params(self, harmony_item, chord_item, preview: bool = False):
        if self.sequencer_widget.is_key_step_button_pressed():
            self.params.set_ranges(selected_harmony_items=[harmony_item])
            self.params.set_options(preview=preview)
        elif self.sequencer_widget.is_chord_step_button_pressed():
            self.params.set_ranges(
                selected_harmony_items=[harmony_item],
                selected_chord_items=[chord_item],
            )
            self.params.set_options(
                continuous=True,
                preview=preview,
            )
        else:
            self.params.clear_ranges()
            self.params.set_options(preview=preview)

    def handle_sequencer_widget_stepper_change(self, state):
        harmony_item, chord_item = self.composer_grid.get_current_items()

        self.set_params(harmony_item, chord_item)

        self.update_frame_display()

    def handle_sequencer_widget_play_button(self, state):
        self.manager.sequencer.grid_play.emit()

    def handle_chord_item_change_from_chord_picker(self, chord_item):
        self.composer_grid.update_chord_item(chord_item)

        is_playing = self.manager.sequencer.is_playing()
        is_playing_preview = self.manager.sequencer.is_playing_preview()

        harmony_item, chord_item = self.composer_grid.get_current_items()

        self.set_params(
            harmony_item, chord_item, preview=not is_playing or is_playing_preview
        )
        self.params.set_first_items(harmony_item, chord_item)

        self.manager.sequencer.grid_play.emit()

        self.update_frame_display()

    def handle_scale_change(self, scale):
        self.composer_grid.harmony_grid.update_item_scale(scale)

        self.update_frame_display()

    def handle_time_signature_change(self, time_signature):
        self.composer_grid.harmony_grid.update_item_time_signature(time_signature)

    def handle_bpm_change(self, bpm):
        self.composer_grid.harmony_grid.update_item_bpm(bpm)

    def handle_harmony_item_change_from_grid(self, harmony_item, chord_item):
        self.scale_selector.set(harmony_item.scale)
        self.chord_picker.set(chord_item)

        self.time_signature_selector.set(harmony_item.time_signature)
        self.bpm_spinbox.set(harmony_item.bpm)

        self.update_frame_display()

    def handle_chord_item_change_from_grid(self, chord_item: ChordItem):
        self.chord_picker.set(chord_item)

        self.update_frame_display()

    def get_next_items(self) -> Tuple[HarmonyItem, ChordItem]:
        harmony_item, chord_item = self.composer_grid.get_current_items()
        chord_items = harmony_item.chord_items

        chord_index = chord_item.get_index_from(chord_items)
        next_chord_index = chord_index + 1

        if (
            self.sequencer_widget.is_chord_step_button_pressed()
            or self.sequencer_widget.is_key_step_button_pressed()
        ):
            return harmony_item, chord_items[next_chord_index % len(chord_items)]

        if next_chord_index >= len(chord_items):
            harmony_items = self.composer_grid.harmony_grid.get_items()

            harmony_index = harmony_item.get_index_from(harmony_items)
            next_harmony_index = harmony_index + 1

            next_harmony_item = harmony_items[next_harmony_index % len(harmony_items)]

            return next_harmony_item, next_harmony_item.chord_items[0]

        return harmony_item, chord_items[next_chord_index]

    def update_frame_display(self):
        self.harmony_chord_frames.update_frames(
            current_items=self.composer_grid.get_current_items(),
            next_items=self.get_next_items(),
        )
