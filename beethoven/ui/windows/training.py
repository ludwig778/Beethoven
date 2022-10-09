from random import shuffle
from typing import List, Protocol

from PySide6.QtWidgets import QWidget, QComboBox, QStackedLayout

from beethoven.helpers.chord import chord_product
from beethoven.helpers.scale import scale_product
from beethoven.models.notes import Notes
from beethoven.ui.checker import NoteCheckerType, NotesContainerChecker
from beethoven.ui.components.buttons import Button, PushPullButton
from beethoven.ui.components.combobox import MidiInputComboBox
from beethoven.ui.components.frame import FramedChord, FramedNotes, FramedScale
from beethoven.ui.components.selectors import ExclusiveScaleSelector, MultipleChordSelector, MultipleNoteSelector
from beethoven.ui.layouts import Stretch, horizontal_layout, vertical_layout
from beethoven.ui.managers import AppManager


class CannotSetupChecker(Exception):
    pass


class BaseTrainingWidget(QWidget):
    def __init__(self, *args, manager: AppManager, **kwargs):
        super(BaseTrainingWidget, self).__init__(*args, **kwargs)

        self.manager = manager
        self.notes_checker = None

        self.start_button = PushPullButton(
            pressed="Playing", released="Start", state=False, object_name="start_button"
        )
        self.stop_button = Button("Stop", object_name="stop_button")

        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)

    def notes_changed(self, notes):
        print("CHANGED LMAO")
        print(notes)
        print(self.notes_checker.current.notes)
        # self.playing_notes_frame.set_notes(notes.values())

        if not self.notes_checker or self.notes_checker.done:
            return

        if self.notes_checker.check(notes):
            if self.notes_checker.done:
                self.target_chord_frame.clear()
                self.start_button.setChecked(False)
            elif self.notes_checker.current:
                self.update_frames()

    def get_buttons(self):
        return horizontal_layout(
            Stretch(),
            self.start_button,
            self.stop_button,
        )

    def start(self):
        print("START ARGS")
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

        self.note_selector = MultipleNoteSelector()
        self.chord_selector = MultipleChordSelector()

        self.target_notes_frame = FramedNotes()
        self.target_chord_frame = FramedChord()

        self.setLayout(
            vertical_layout(
                horizontal_layout(self.note_selector, self.chord_selector),
                horizontal_layout(
                    self.target_notes_frame,
                    self.target_chord_frame,
                ),
                Stretch(),
                self.get_buttons(),
            )
        )

    def setup_note_checker(self):
        notes = self.note_selector.get_checked_notes()
        chord_names = self.chord_selector.get_checked_texts()

        if not (notes and chord_names):
            self.stop()

            return

        chord_list = chord_product(notes, chord_names)
        shuffle(chord_list)

        self.notes_checker = NotesContainerChecker(
            notes_containers=chord_list, type_check=NoteCheckerType.BY_BASE_NOTE
        )
        self.update_frames()

    def update_frames(self):
        self.target_notes_frame.set_notes(self.notes_checker.current.notes)
        self.target_chord_frame.set_chord(self.notes_checker.current)

    def clear_frames(self):
        self.target_notes_frame.clear()
        self.target_chord_frame.clear()


class ScaleTrainingWidget(BaseTrainingWidget):
    title = "Scale Training"

    def __init__(self, *args, **kwargs):
        super(ScaleTrainingWidget, self).__init__(*args, **kwargs)

        self.note_selector = MultipleNoteSelector()
        self.scale_selector = ExclusiveScaleSelector()

        self.target_notes_frame = FramedNotes()
        self.target_scales_frame = FramedScale()

        self.setLayout(
            vertical_layout(
                horizontal_layout(self.note_selector, self.scale_selector),
                horizontal_layout(self.target_notes_frame, self.target_scales_frame),
                self.get_buttons(),
            )
        )

    def setup_note_checker(self):
        notes = self.note_selector.get_checked_notes()
        scale_names = self.scale_selector.get_checked_texts()

        if not (notes and scale_names):
            self.stop()

            return

        print(notes, scale_names)

        scale_list = scale_product(notes, scale_names)
        shuffle(scale_list)

        note_containers = [
            Notes(notes=[note], object=scale)
            for scale in scale_list
            for note in scale.notes
        ]

        self.notes_checker = NotesContainerChecker(
            notes_containers=note_containers, type_check=NoteCheckerType.BY_BASE_NOTE
        )
        self.update_frames()

    def update_frames(self):
        self.target_notes_frame.set_notes(self.notes_checker.current.notes)
        self.target_scales_frame.set_scale(self.notes_checker.current.object)

    def clear_frames(self):
        self.target_notes_frame.set_notes(self.notes_checker.current.notes)
        self.target_scales_frame.set_scale(self.notes_checker.current.object)


class ArppegioTrainingWidget(BaseTrainingWidget):
    title = "Arppegio Training"

    def __init__(self, *args, **kwargs):
        super(ArppegioTrainingWidget, self).__init__(*args, **kwargs)

        self.note_selector = MultipleNoteSelector()
        self.chord_selector = MultipleChordSelector()

        self.target_notes_frame = FramedNotes()
        self.target_chords_frame = FramedChord()

        self.setLayout(
            vertical_layout(
                horizontal_layout(self.note_selector, self.chord_selector),
                horizontal_layout(self.target_notes_frame, self.target_chords_frame),
                self.get_buttons(),
            )
        )

    def setup_note_checker(self):
        notes = self.note_selector.get_checked_notes()
        chord_names = self.chord_selector.get_checked_texts()

        if not (notes and chord_names):
            self.stop()

            return

        print(notes, chord_names)

        chord_list = chord_product(notes, chord_names)
        shuffle(chord_list)

        note_containers = [
            Notes(notes=[note], object=scale)
            for scale in chord_list
            for note in scale.notes
        ]

        self.notes_checker = NotesContainerChecker(
            notes_containers=note_containers, type_check=NoteCheckerType.BY_BASE_NOTE
        )
        self.update_frames()

    def update_frames(self):
        self.target_notes_frame.set_notes(self.notes_checker.current.notes)
        self.target_chords_frame.set_chord(self.notes_checker.current.object)

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
        **kwargs
    ):
        super(TrainingWindow, self).__init__(*args, **kwargs)

        self.setFixedSize(400, 400)

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
            vertical_layout([
                self.input_combobox,
                self.combobox,
                self.training_layout,
                # Stretch()
            ])
        )

    def notes_changed(self, notes):
        print("CHANGED")
        return self.training_widget.notes_changed(notes)

    def changed_midi_input(self, text):
        self.manager.input_handler.set_input(text)

    def update_training(self, string):
        if self.training_widget:
            self.training_layout.removeWidget(self.training_widget)

        training_widget_class = self.training_widgets.get(string)
        training_widget = training_widget_class(manager=self.manager, parent=self)
        training_widget.style().unpolish(training_widget)
        training_widget.style().polish(training_widget)

        self.training_widget = training_widget
        self.training_layout.addWidget(self.training_widget)
