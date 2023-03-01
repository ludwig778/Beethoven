import logging
from random import shuffle
from typing import Callable, List, Optional, Protocol, cast

from PySide6.QtWidgets import QComboBox, QStackedLayout, QWidget

from beethoven.models import Chord, NotesList, Scale
from beethoven.ui.checker import NoteCheckerType, NotesContainerChecker
from beethoven.ui.components.buttons import Button, PushPullButton
from beethoven.ui.components.combobox import MidiInputComboBox
from beethoven.ui.components.frame import FramedChord, FramedScale
from beethoven.ui.components.selectors import (
    ChordMultipleSelector,
    NoteMultipleSelector,
    ScaleExclusiveSelector,
)
from beethoven.ui.layouts import Stretch, horizontal_layout, vertical_layout
from beethoven.ui.managers import AppManager

logger = logging.getLogger("app.trainers")


class CannotSetupChecker(Exception):
    pass


class BaseTrainingWidget(QWidget):
    def __init__(self, *args, manager: AppManager, **kwargs):
        super(BaseTrainingWidget, self).__init__(*args, **kwargs)

        self.manager = manager
        self.notes_checker: Optional[NotesContainerChecker] = None

        self.start_button = PushPullButton("Start", pressed=False, pressed_text="Playing")
        self.stop_button = Button("Stop", object_name="stop_button")

        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)

    def notes_changed(self, notes):
        # if self.notes_checker and (current := self.notes_checker.current):
        #     logger.info(current.notes)
        # self.playing_notes_frame.set_notes(notes.values())

        if not self.notes_checker or self.notes_checker.done:
            return

        if self.notes_checker.check(NotesList(notes=notes)):
            if self.notes_checker.done:
                self.target_chord_frame.clear()
                self.start_button.setChecked(False)
            elif self.notes_checker.current:
                self.update_frames()

    def get_buttons(self):
        return horizontal_layout(
            [
                Stretch(),
                self.start_button,
                self.stop_button,
            ]
        )

    def start(self):
        if not self.start_button.isChecked():
            self.stop()

            return

        self.setup_note_checker()

    def stop(self):
        self.notes_checker = None
        self.start_button.setChecked(False)

        self.clear_frames()


class ChordTrainingWidget(BaseTrainingWidget):
    title = "Chord Training"

    def __init__(self, *args, **kwargs):
        super(ChordTrainingWidget, self).__init__(*args, **kwargs)

        self.note_selector = NoteMultipleSelector()
        self.chord_selector = ChordMultipleSelector()

        # self.target_notes_frame = FramedNotes()
        self.target_chord_frame = FramedChord()

        self.setLayout(
            vertical_layout(
                [
                    horizontal_layout([self.note_selector, self.chord_selector]),
                    horizontal_layout(
                        [
                            self.target_notes_frame,
                            self.target_chord_frame,
                        ]
                    ),
                    Stretch(),
                    self.get_buttons(),
                ]
            )
        )

    def setup_note_checker(self):
        notes = self.note_selector.get_checked_notes()
        chord_names = self.chord_selector.get_checked_texts()

        if not (notes and chord_names):
            self.stop()

            return

        chord_list = Chord.chord_product(notes, chord_names)
        shuffle(chord_list)

        self.notes_checker = NotesContainerChecker(
            notes_containers=chord_list, type_check=NoteCheckerType.BY_BASE_NOTE
        )
        self.update_frames()

    def update_frames(self):
        if self.notes_checker and (current := self.notes_checker.current) and isinstance(current, Chord):
            self.target_notes_frame.set_notes(current.notes)
            self.target_chord_frame.set_chord(current.object)

    def clear_frames(self):
        self.target_notes_frame.clear()
        self.target_chord_frame.clear()


class ScaleTrainingWidget(BaseTrainingWidget):
    title = "Scale Training"

    def __init__(self, *args, **kwargs):
        super(ScaleTrainingWidget, self).__init__(*args, **kwargs)

        self.note_selector = NoteMultipleSelector()
        self.scale_selector = ScaleExclusiveSelector()

        # self.target_notes_frame = FramedNotes()
        self.target_scale_frame = FramedScale()

        self.setLayout(
            vertical_layout(
                [
                    horizontal_layout([self.note_selector, self.scale_selector]),
                    horizontal_layout([self.target_notes_frame, self.target_scale_frame]),
                    self.get_buttons(),
                ]
            )
        )

    def setup_note_checker(self):
        notes = self.note_selector.get_checked_notes()
        scale_names = self.scale_selector.get_checked_texts()

        if not (notes and scale_names):
            self.stop()

            return

        scale_list = Scale.scale_product(notes, scale_names)
        shuffle(scale_list)

        note_containers = [scale for scale in scale_list]

        self.notes_checker = NotesContainerChecker(
            notes_containers=note_containers, type_check=NoteCheckerType.BY_BASE_NOTE
        )
        self.update_frames()

    def update_frames(self):
        if self.notes_checker and (current := self.notes_checker.current) and isinstance(current, Scale):
            self.target_notes_frame.set_notes(current.notes)
            self.target_scale_frame.set_scale(current)

    def clear_frames(self):
        self.target_notes_frame.clear()
        self.target_scale_frame.clear()


class ArppegioTrainingWidget(BaseTrainingWidget):
    title = "Arppegio Training"

    def __init__(self, *args, **kwargs):
        super(ArppegioTrainingWidget, self).__init__(*args, **kwargs)

        self.note_selector = NoteMultipleSelector()
        self.chord_selector = ChordMultipleSelector()

        # self.target_notes_frame = FramedNotes()
        self.target_chords_frame = FramedChord()

        self.setLayout(
            vertical_layout(
                [
                    horizontal_layout([self.note_selector, self.chord_selector]),
                    horizontal_layout([self.target_notes_frame, self.target_chords_frame]),
                    self.get_buttons(),
                ]
            )
        )

    def setup_note_checker(self):
        notes = self.note_selector.get_checked_notes()
        chord_names = self.chord_selector.get_checked_texts()

        if not (notes and chord_names):
            self.stop()

            return

        chord_list = Chord.chord_product(notes, chord_names)
        shuffle(chord_list)

        note_containers = [chord for chord in chord_list]

        self.notes_checker = NotesContainerChecker(
            notes_containers=note_containers, type_check=NoteCheckerType.BY_BASE_NOTE
        )
        self.update_frames()

    def update_frames(self):
        if self.notes_checker and (current := self.notes_checker.current) and isinstance(current, Chord):
            self.target_notes_frame.set_notes(current.notes)
            self.target_chords_frame.set_chord(current.object)

    def clear_frames(self):
        self.target_notes_frame.clear()
        self.target_chords_frame.clear()


training_widgets = [
    ChordTrainingWidget,
    ScaleTrainingWidget,
    ArppegioTrainingWidget,
]


class TrainingWidget(Protocol):
    @property
    def title(self):
        ...


class TrainingWindow(QWidget):
    def __init__(
        self,
        *args,
        manager: AppManager,
        training_widgets: List[TrainingWidget],
        initial_widget: TrainingWidget,
        **kwargs,
    ):
        super(TrainingWindow, self).__init__(*args, **kwargs)

        self.manager = manager
        self.training_widgets = {widget.title: widget for widget in training_widgets}

        self.input_combobox = MidiInputComboBox(
            manager=self.manager, value=self.manager.settings.midi.selected_input
        )
        self.input_combobox.currentTextChanged.connect(self.changed_midi_input)

        self.manager.input_handler.notes_changed.connect(self.notes_changed)

        self.combobox = QComboBox()
        self.combobox.addItems(list(self.training_widgets.keys()))

        self.training_layout = QStackedLayout()
        self.training_widget = None

        self.update_training(initial_widget.title)
        self.combobox.setCurrentText(initial_widget.title)

        self.combobox.currentTextChanged.connect(self.update_training)

        self.setLayout(
            vertical_layout(
                [
                    self.input_combobox,
                    self.combobox,
                    self.training_layout,
                ]
            )
        )

    def notes_changed(self, notes):
        return self.training_widget.notes_changed(notes)

    def changed_midi_input(self, text):
        self.manager.input_handler.set_input(text)

    def update_training(self, string):
        if self.training_widget:
            self.training_layout.removeWidget(self.training_widget)

        training_widget_class = self.training_widgets.get(string)
        training_widget = cast(Callable, training_widget_class)(manager=self.manager)
        training_widget.style().unpolish(training_widget)
        training_widget.style().polish(training_widget)

        self.training_widget = training_widget
        self.training_layout.addWidget(cast(QWidget, self.training_widget))
