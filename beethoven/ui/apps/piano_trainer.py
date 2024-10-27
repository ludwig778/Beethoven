import logging

from PySide6.QtWidgets import QWidget

from beethoven.models import Chord
from beethoven.ui.checker import NoteCheckerType, NotesContainerChecker
from beethoven.ui.components.buttons import Button, PushPullButton
from beethoven.ui.components.frame import FramedChord, FramedNote
from beethoven.ui.components.selectors import (ChordMultipleSelector,
                                               NoteMultipleSelector)
from beethoven.ui.layouts import Stretch, horizontal_layout, vertical_layout
from beethoven.ui.managers import AppManager

logger = logging.getLogger("app.compose")


class PianoTrainerWidget(QWidget):
    def __init__(self, *args, manager: AppManager, **kwargs):
        super(PianoTrainerWidget, self).__init__(*args, **kwargs)

        self.manager = manager

        self.notes_checker: NotesContainerChecker | None = None

        self.playing_notes_frame = FramedNote()
        self.target_chord_frame = FramedChord()

        self.chord_selector = ChordMultipleSelector()
        self.note_selector = NoteMultipleSelector()

        self.start_button = PushPullButton("Playing", pressed_text="Start")
        self.start_button.setObjectName("start_button")

        self.stop_button = Button("Stop")
        self.stop_button.setObjectName("stop_button")

        self.manager.midi.notes_changed.connect(self.notes_changed)
        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)

        self.setLayout(
            vertical_layout(
                [
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

    def setup(self):
        logger.info("setup")

    def teardown(self):
        logger.info("teardown")

    def notes_changed(self, notes):
        print("notes_changed", notes)

        notes = dict(notes)

        self.playing_notes_frame.set_notes(notes.values())

        if not self.notes_checker or self.notes_checker.done:
            return

        if self.notes_checker.check(notes):
            if self.notes_checker.done:
                self.target_chord_frame.clear()
                self.start_button.setChecked(False)
            elif isinstance(self.notes_checker.current, Chord):
                print(self.notes_checker.current)
                self.target_chord_frame.set_chord(self.notes_checker.current)

    def start(self, *args):
        print("Start", args)
        """
        if not self.start_button.isChecked():
            self.stop()

            return
        """

        notes = self.note_selector.get_checked_notes()
        chord_names = self.chord_selector.get_checked_texts()

        if not (notes and chord_names):
            self.stop()

            return

        chord_list = Chord.chord_product(notes, chord_names)
        # shuffle(chord_list)

        self.notes_checker = NotesContainerChecker(
            notes_containers=chord_list, type_check=NoteCheckerType.BY_BASE_NOTE
        )

        if isinstance(self.notes_checker.current, Chord):
            print(self.notes_checker.current)
            self.target_chord_frame.set_chord(self.notes_checker.current)

    def stop(self):
        print("Stop")
        self.target_chord_frame.clear()
        self.start_button.setChecked(False)
