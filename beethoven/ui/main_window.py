from typing import List

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow

from beethoven.models import (Bpm, ChordItem, Degree, Duration, DurationItem,
                              HarmonyItem, Scale, TimeSignature)
from beethoven.ui.apps.compose import ComposeWidget
# from beethoven.ui.apps.harmony_trainer import HarmonyTrainerWidget
# from beethoven.ui.apps.harmony_trainer import HarmonyTrainerWidget
from beethoven.ui.apps.piano_trainer import PianoTrainerWidget
from beethoven.ui.components.combobox.widget_selector import \
    WidgetSelectorComboBox
from beethoven.ui.managers import AppManager


class MainWindow(QMainWindow):
    def __init__(self, *args, manager: AppManager, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Beethoven")

        self.manager = manager

        self.set_menubar()

        def gen_harmony_items() -> List[HarmonyItem]:
            base_duration = Duration.parse("Q")

            harmony_items = []
            for scale_str, bpm_str, time_signature_str, chords in [
                (
                    "C4_major",
                    "90",
                    "4/4",
                    [
                        ("I", Duration.parse("6Q")),
                        ("II", None),
                    ],
                ),
                # (
                #     "A4_minor",
                #     "90",
                #     "7/8",
                #     [
                #         ("IV", Duration.parse("3Q")),
                #         ("V", Duration.parse("2Q")),
                #         ("VI", None),
                #     ],
                # ),
                # (
                #     "E4_major",
                #     "80",
                #     "7/4",
                #     [("IV", Duration.parse("4Q"))],
                # ),
            ]:
                scale = Scale.parse(scale_str)
                bpm = Bpm.parse(bpm_str)
                time_signature = TimeSignature.parse(time_signature_str)

                harmony_item = HarmonyItem(scale=scale, chord_items=[], bpm=bpm, time_signature=time_signature)
                harmony_items.append(harmony_item)

                for chord, duration in chords:
                    # chord = Chord.parse_with_scale_context(chord, scale=scale)

                    if duration:
                        numerator = duration.value // base_duration.value

                        duration_item = DurationItem(numerator=numerator, base_duration=base_duration)
                    else:
                        duration_item = DurationItem()

                    # chord_item = ChordItem(root=chord, name=chord.name, duration_item=duration_item)
                    chord_item = ChordItem(root=Degree.parse(chord), name="", duration_item=duration_item)
                    harmony_item.chord_items.append(chord_item)

            return harmony_items

        # harmony_items = gen_harmony_items()

        self.stack = WidgetSelectorComboBox(
            widgets=[
                ("Compose", ComposeWidget(manager=manager)),  # , harmony_items=harmony_items)),
                ("Piano Training", PianoTrainerWidget(manager=manager)),
                # ("Harmony Trainer", HarmonyTrainerWidget(manager=manager)),
            ],
            selected_index=0,
        )
        self.stack.setup()
        self.stack.setContentsMargins(6, 6, 6, 6)

        self.setCentralWidget(self.stack)

    def set_menubar(self):
        menubar = self.menuBar()

        file = menubar.addMenu("File")

        quit = QAction("Quit", self)
        quit.setShortcut("Q")
        quit.triggered.connect(self.close)

        file.addAction(quit)

    def run_dialog(self, dialog_class, **kwargs):
        def setup_dialog():
            dialog = dialog_class(**kwargs)
            dialog.exec()

        return setup_dialog
