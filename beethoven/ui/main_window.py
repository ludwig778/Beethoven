from random import shuffle

from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)
from beethoven import controllers

from beethoven.helpers.chord import chord_product
from beethoven.models.grid import Grid
from beethoven.models.grid_part import GridPart
from beethoven.ui.checker import NoteCheckerType, NotesContainerChecker
from beethoven.ui.components.buttons import Button, PushPullButton
from beethoven.ui.components.chord_picker import ChordPicker
from beethoven.ui.components.combobox import MidiInputComboBox
from beethoven.ui.components.control import PlayerControlWidget, PlayingType
from beethoven.ui.components.frame import FramedChord, FramedNotes
from beethoven.ui.components.harmony_grid import HarmonyGrid
from beethoven.ui.components.scale_picker import ScalePicker
from beethoven.ui.components.selectors import (
    MultipleChordSelector,
    MultipleNoteSelector,
)
from beethoven.ui.constants import INITIAL_GRID_PART
from beethoven.ui.layouts import horizontal_layout, vertical_layout
from beethoven.ui.managers import AppManager
from beethoven.ui.models import HarmonyItems


class Widget(QWidget):
    def __init__(self, i, *args, **kwargs):
        super(Widget, self).__init__(*args, **kwargs)

        self.i = i
        self.setLayout(self.get_layout())

    def get_layout(self):
        main_layout = QVBoxLayout()

        for _ in range(4):
            main_layout.addWidget(QLabel(f"Label {self.i}"))

        return main_layout


class ComposeWidget(QWidget):
    # def __init__(self, *args, manager: AppManager, harmony_items: HarmonyItems, **kwargs):
    def __init__(self, *args, manager: AppManager, **kwargs):
        super(ComposeWidget, self).__init__(*args, **kwargs)

        self.manager = manager

        harmony_items = HarmonyItems.from_list([
            {
                "scale": "C4_ionian",
                "chord_items": [
                    {"root": "I", "name": ""},
                    # {"root": "III", "name": "maj7"},
                    # {"root": "A", "name": ""},
                    # {"root": "D", "name": ""},
                    # {"root": "E", "name": ""},
                ]
            },
        ])

        self.harmony_grid = HarmonyGrid(
            manager=manager,
            harmony_items=harmony_items
        )
        self.harmony_grid.harmony_item_changed.connect(self.update_harmony)
        self.harmony_grid.chord_item_changed.connect(self.update_chord)

        harmony_item, chord_item = self.harmony_grid.get_current_item()

        self.player_widget = PlayerControlWidget(
            harmony_items=harmony_items,
            playing_type=PlayingType.step
        )

        self.chord_picker = ChordPicker(
            manager=manager,
            current_chord_item=chord_item,
            current_scale=harmony_item.scale,
        )
        self.scale_selector = ScalePicker(
            current_scale=harmony_item.scale
        )

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
            initial_state=INITIAL_GRID_PART,
            parts=[
                GridPart(
                    scale=harmony_item.scale,
                    chord=chord_item.as_chord(scale=harmony_item.scale),
                    duration=controllers.duration.parse("4W")
                )
            ]
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


class TrainingWidget(QWidget):
    def __init__(self, *args, manager: AppManager, **kwargs):
        super(TrainingWidget, self).__init__(*args, **kwargs)

        self.manager = manager

        self.notes_checker = None

        self.setup()

    def setup(self):
        self.input_combobox = MidiInputComboBox(
            manager=self.manager, value=self.manager.settings.midi.selected_input
        )

        self.playing_notes_frame = FramedNotes()
        self.target_chord_frame = FramedChord()

        self.chord_selector = MultipleChordSelector()
        self.note_selector = MultipleNoteSelector()

        self.start_button = PushPullButton(
            pressed="Playing", released="Start", state=False, object_name="start_button"
        )
        self.stop_button = Button("Stop", object_name="stop_button")

        self.input_combobox.currentTextChanged.connect(self.changed_midi_input)
        self.manager.midi.notes_changed.connect(self.notes_changed)
        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)

        self.setLayout(self.get_layout())

    def get_layout(self):
        main_layout = QVBoxLayout()

        control_buttons = QHBoxLayout()
        control_buttons.addStretch()
        control_buttons.addWidget(self.start_button)
        control_buttons.addWidget(self.stop_button)

        note_frames = QHBoxLayout()
        note_frames.addWidget(self.playing_notes_frame)
        note_frames.addWidget(self.target_chord_frame)

        selectors = QHBoxLayout()
        selectors.addWidget(self.chord_selector)
        selectors.addWidget(self.note_selector)

        main_layout.addWidget(QLabel("Training"))
        main_layout.addWidget(self.input_combobox)
        main_layout.addLayout(selectors)
        main_layout.addLayout(note_frames)
        main_layout.addStretch()
        main_layout.addLayout(control_buttons)

        return main_layout

    def notes_changed(self, notes):
        self.playing_notes_frame.set_notes(notes.values())

        if not self.notes_checker or self.notes_checker.done:
            return

        if self.notes_checker.check(notes):
            if self.notes_checker.done:
                self.target_chord_frame.clear()
                self.start_button.setChecked(False)
            elif current_chord := self.notes_checker.current:
                self.target_chord_frame.set_chord(current_chord)

    def changed_midi_input(self, input_name):
        self.manager.midi.update_input(input_name)
        self.manager.midi.notes_changed.emit({})

    def start(self, *args):
        print("START ARGS", args)
        if not self.start_button.isChecked():
            self.stop()

            return

        notes = self.note_selector.get_checked_notes()
        chord_names = self.chord_selector.get_checked_texts()
        print(notes, chord_names)

        if not (notes and chord_names):
            self.stop()

            return

        chord_list = chord_product(notes, chord_names)
        shuffle(chord_list)

        self.notes_checker = NotesContainerChecker(
            notes_containers=chord_list, type_check=NoteCheckerType.BY_BASE_NOTE
        )

        self.target_chord_frame.set_chord(self.notes_checker.current)

    def stop(self):
        self.target_chord_frame.clear()
        self.start_button.setChecked(False)


class MainWindow(QMainWindow):
    def __init__(self, *args, manager: AppManager, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.manager = manager

        self.setCentralWidget(self.get_central_widget())

        self.setFixedSize(500, 500)

    def get_central_widget(self):
        widget = QWidget()

        main_layout = QVBoxLayout()

        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(TrainingWidget(manager=self.manager))
        self.stacked_layout.addWidget(ComposeWidget(manager=self.manager))

        button_layout = QHBoxLayout()

        ok_button = QPushButton("Ok")
        training_button = QPushButton("Training")
        compose_button = QPushButton("Compose")

        button_layout.addWidget(ok_button)
        button_layout.addWidget(training_button)
        button_layout.addWidget(compose_button)

        main_layout.addLayout(self.stacked_layout)
        main_layout.addLayout(button_layout)

        widget.setLayout(main_layout)

        for button in [ok_button, training_button, compose_button]:
            button.setStyleSheet("height:33px;")

        ok_button.clicked.connect(self.close)
        training_button.clicked.connect(lambda: self.set_widget(0))
        compose_button.clicked.connect(lambda: self.set_widget(1))

        return widget

    def set_widget(self, index):
        """
        print("SET STACKED", [index])
        print(self.stacked_layout.currentIndex())
        """

        self.stacked_layout.setCurrentIndex(int(index))
