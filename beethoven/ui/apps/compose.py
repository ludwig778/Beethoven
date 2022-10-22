from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QWidget

from beethoven import controllers
from beethoven.models.grid import Grid
from beethoven.models.grid_part import GridPart
from beethoven.ui.components.chord_picker import ChordPicker
from beethoven.ui.components.control import PlayerControlWidget, PlayingType
from beethoven.ui.components.composer_grid import ComposerGrid
from beethoven.ui.components.scale_picker import ScalePicker
from beethoven.ui.layouts import horizontal_layout, vertical_layout
from beethoven.ui.managers import AppManager
from beethoven.ui.models import HarmonyItems
from beethoven.ui.utils import get_default_harmony_items


class ComposeWidget(QWidget):
    def __init__(
        self,
        *args,
        manager: AppManager,
        harmony_items: HarmonyItems = get_default_harmony_items(),
        **kwargs
    ):
        super(ComposeWidget, self).__init__(*args, **kwargs)

        self.manager = manager

        self.composer_grid = ComposerGrid(manager=manager, harmony_items=harmony_items)
        self.composer_grid.harmony_item_changed.connect(self.update_harmony)
        self.composer_grid.chord_item_changed.connect(self.update_chord)

        harmony_item, chord_item = self.composer_grid.get_current_item()

        self.player_widget = PlayerControlWidget(
            harmony_items=harmony_items, playing_type=PlayingType.step
        )

        self.chord_picker = ChordPicker(
            manager=manager,
            current_chord_item=chord_item,
            current_scale=harmony_item.scale,
        )
        self.scale_selector = ScalePicker(current_scale=harmony_item.scale)

        self.chord_picker.chord_item_changed.connect(self.selected_chord_item_changed)
        self.scale_selector.scale_changed.connect(self.selected_scale_changed)

        self.player_widget.play_grid_step.connect(self.play_current_item)
        self.player_widget.stop_grid.connect(self.stop)

        self.action_binding = QShortcut(QKeySequence("Space"), self)
        self.action_binding.activated.connect(self.handle_binding_action)

        self.setLayout(
            vertical_layout(
                [
                    self.chord_picker,
                    horizontal_layout(
                        [
                            self.scale_selector,
                            self.player_widget,
                        ]
                    ),
                    self.composer_grid,
                ]
            )
        )

    def play_current_item(self, continuous: bool = False):
        harmony_item, chord_item = self.composer_grid.get_current_item()

        grid = Grid(
            parts=[
                GridPart(
                    scale=harmony_item.scale,
                    chord=chord_item.as_chord(scale=harmony_item.scale),
                    bpm=controllers.bpm.parse("90"),
                    time_signature=controllers.time_signature.parse("4/4"),
                    duration=controllers.duration.parse("160W" if continuous else "1W"),
                )
            ]
        )
        self.manager.play_grid(grid, preview=True)

    def stop(self):
        self.manager.midi.terminate_output_thread()

    def handle_binding_action(self):
        self.composer_grid.next()

        self.play_current_item(continuous=True)

    def selected_chord_item_changed(self, chord_item):
        self.composer_grid.update_current_chord(chord_item)

        self.play_current_item()

    def selected_scale_changed(self, scale):
        self.composer_grid.update_current_scale(scale)

        self.play_current_item()

    def update_harmony(self):
        harmony_item, chord_item = self.composer_grid.get_current_item()

        self.scale_selector.set_scale(harmony_item.scale)
        self.chord_picker.set_chord_item(chord_item)

    def update_chord(self):
        _, chord_item = self.composer_grid.get_current_item()

        self.chord_picker.set_chord_item(chord_item)
