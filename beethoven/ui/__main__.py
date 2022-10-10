import atexit
from pathlib import Path
from logging import getLogger
from beethoven import controllers
from beethoven.models.grid import Grid
from beethoven.models.grid_part import GridPart
from beethoven.ui.components.chord_picker import ChordPicker
from beethoven.ui.components.control import PlayerControlWidget, PlayingType
from beethoven.ui.components.harmony_grid import HarmonyGrid
from beethoven.ui.components.scale_picker import ScalePicker
from beethoven.ui.layouts import horizontal_layout, vertical_layout
from beethoven.ui.managers import AppManager
from beethoven.ui.models import HarmonyItems
from beethoven.ui.stylesheet import get_stylesheet
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QWidget, QApplication

logger = getLogger("ui.main")


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
