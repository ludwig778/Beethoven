from typing import List

from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QLabel, QWidget

from beethoven.models import Duration, Grid, GridPart
from beethoven.ui.components.composer_grid import ComposerGrid
from beethoven.ui.components.control import PlayerControl
from beethoven.ui.components.scale_picker import ScalePicker
from beethoven.ui.components.selectors.time_signature import TimeSignatureSelector
from beethoven.ui.components.spinbox import BpmSpinBox
from beethoven.ui.dialogs.chord_picker import ChordPickerDialog
from beethoven.ui.layouts import Spacing, Stretch, horizontal_layout, vertical_layout
from beethoven.ui.managers import AppManager
from beethoven.ui.models import ChordItem, HarmonyItem
from beethoven.ui.utils import (
    connect_push_pull_button_and_dialog,
    get_default_harmony_items,
)


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

        self.composer_grid = ComposerGrid(harmony_items=harmony_items)
        self.composer_grid.harmony_item_changed.connect(self.update_harmony)
        self.composer_grid.chord_item_changed.connect(self.update_chord)

        harmony_item, chord_item = self.composer_grid.get_current_item()

        self.player_widget = PlayerControl()

        self.chord_picker = ChordPickerDialog(chord_item=chord_item)

        connect_push_pull_button_and_dialog(
            self.composer_grid.chord_grid.modify_button, self.chord_picker
        )

        self.scale_selector = ScalePicker(scale=harmony_item.scale)
        self.time_signature_selector = TimeSignatureSelector()
        self.bpm_spinbox = BpmSpinBox()

        self.chord_picker.value_changed.connect(self.handle_chord_item_change)
        self.scale_selector.value_changed.connect(self.handle_scale_change)
        self.time_signature_selector.value_changed.connect(
            self.handle_time_signature_change
        )
        self.bpm_spinbox.value_changed.connect(self.handle_bpm_change)

        self.player_widget.play_grid_chord_step.connect(self.play_current_item)
        self.player_widget.stop_grid.connect(self.stop)

        self.action_binding = QShortcut(QKeySequence("Space"), self)
        self.action_binding.activated.connect(self.handle_binding_action)  # type: ignore

        self.setLayout(
            vertical_layout(
                [
                    Spacing(size=3),
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
                    self.composer_grid,
                    Stretch(),
                ],
            )
        )

    # TODO
    def play_current_item(self, continuous: bool = False):
        harmony_item, chord_item = self.composer_grid.get_current_item()

        grid = Grid(
            parts=[
                GridPart(
                    scale=harmony_item.scale,
                    chord=chord_item.as_chord(scale=harmony_item.scale),
                    bpm=harmony_item.bpm,
                    time_signature=harmony_item.time_signature,
                    duration=Duration.parse("160W" if continuous else "1W"),
                )
            ]
        )
        self.manager.play_grid(grid, preview=True)

    def stop(self):
        self.manager.midi.terminate_output_thread()

    def handle_binding_action(self):
        self.composer_grid.next()

        self.play_current_item(continuous=True)

    def handle_chord_item_change(self, chord_item):
        print("chord_item", chord_item)
        self.composer_grid.update_chord_item(chord_item)

        self.play_current_item()

    def handle_scale_change(self, scale):
        self.composer_grid.harmony_grid.update_item_scale(scale)

        self.play_current_item()

    def handle_time_signature_change(self, time_signature):
        self.composer_grid.harmony_grid.update_item_time_signature(time_signature)

        # self.play_current_item()

    def handle_bpm_change(self, bpm):
        self.composer_grid.harmony_grid.update_item_bpm(bpm)

        # self.play_current_item()

    def update_harmony(self):
        harmony_item, chord_item = self.composer_grid.get_current_item()

        self.scale_selector.set(harmony_item.scale)
        self.chord_picker.set(chord_item)

        self.time_signature_selector.set(harmony_item.time_signature)
        self.bpm_spinbox.set(harmony_item.bpm)

    def update_chord(self, chord_item: ChordItem):
        self.chord_picker.set(chord_item)
