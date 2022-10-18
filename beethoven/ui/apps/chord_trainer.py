from random import shuffle

from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from beethoven.helpers.chord import chord_product
from beethoven.ui.checker import NoteCheckerType, NotesContainerChecker
from beethoven.ui.components.buttons import Button, PushPullButton
from beethoven.ui.components.combobox import MidiInputComboBox
from beethoven.ui.components.frame import FramedChord, FramedNotes
from beethoven.ui.components.selectors import (
    MultipleChordSelector,
    MultipleNoteSelector,
)
from beethoven.ui.layouts import Stretch, horizontal_layout, vertical_layout
from beethoven.ui.managers import AppManager


class ChordTrainerWidget(QWidget):
    def __init__(self, *args, manager: AppManager, **kwargs):
        super(ChordTrainerWidget, self).__init__(*args, **kwargs)

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

        self.setLayout(
            vertical_layout(
                [
                    self.input_combobox,
                    horizontal_layout(
                        [
                            self.chord_selector,
                            self.note_selector,
                        ]
                    ),
                    horizontal_layout(
                        [
                            self.playing_notes_frame,
                            self.target_chord_frame,
                        ]
                    ),
                    Stretch(),
                    horizontal_layout(
                        [
                            Stretch(),
                            self.start_button,
                            self.stop_button,
                        ]
                    ),
                ]
            )
        )

    def get_layout(self):
        if True:
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
