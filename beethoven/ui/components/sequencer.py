import logging
from functools import partial
from typing import Optional, Set

from PySide6.QtWidgets import QPushButton, QWidget

from beethoven.ui.components.buttons import PushPullButton
from beethoven.ui.layouts import Spacing, horizontal_layout, vertical_layout
from beethoven.ui.utils import block_signal

logger = logging.getLogger("control")


class SequencerWidget(QWidget):
    def __init__(self, *args, manager, **kwargs):
        super(SequencerWidget, self).__init__(*args, **kwargs)

        self.manager = manager

        self.key_step_button = PushPullButton("Key Step Mode")
        self.chord_step_button = PushPullButton("Chord Step Mode")
        self.play_button = PushPullButton("Play")
        self.stop_button = QPushButton("Stop")

        self.key_step_button.toggled.connect(self.handle_key_step)
        self.chord_step_button.toggled.connect(self.handle_chord_step)

        self.play_button.toggled.connect(self.handle_play)
        self.stop_button.clicked.connect(self.stop)

        self.manager.sequencer.grid_ended.connect(self.release_play)

        self.setLayout(
            vertical_layout(
                [
                    self.key_step_button,
                    Spacing(size=1),
                    self.chord_step_button,
                    Spacing(size=1),
                    horizontal_layout(
                        [
                            self.play_button,
                            self.stop_button,
                        ]
                    ),
                ]
            )
        )

    def setup(self):
        self._set_pressed_play_button_func = partial(self.set_play_button_state, True)
        self._set_release_play_button_func = partial(self.set_play_button_state, False)

        self.manager.sequencer.grid_play.connect(self._set_pressed_play_button_func)
        self.manager.sequencer.grid_stop.connect(self._set_release_play_button_func)

    def teardown(self):
        self.manager.sequencer.grid_play.disconnect(self._set_pressed_play_button_func)
        self.manager.sequencer.grid_stop.disconnect(self._set_release_play_button_func)

        if not self.manager.sequencer.is_stopped():
            self.manager.sequencer.grid_stop.emit()

        self.release_all()

    def is_key_step_button_pressed(self):
        return self.key_step_button.pressed

    def is_chord_step_button_pressed(self):
        return self.chord_step_button.pressed

    def is_play_button_pressed(self):
        return self.play_button.pressed

    def handle_key_step(self, state):
        logger.info(f"harmony step play: {'pressed' if state else 'released'}")

        if self.is_chord_step_button_pressed():
            self.release_all(ignore={self.play_button, self.key_step_button})

    def handle_chord_step(self, state):
        logger.info(f"chord step play: {'pressed' if state else 'released'}")

        if self.is_key_step_button_pressed():
            self.release_all(ignore={self.play_button, self.chord_step_button})

    def handle_play(self, state):
        logger.info(f"play: {'pressed' if state else 'released'}")

        if not state and not self.manager.sequencer.is_stopped():
            self.manager.sequencer.grid_stop.emit()

            logger.info("stop")
        elif state:
            self.manager.sequencer.grid_play.emit()

            logger.info("play")

    def set_play_button_state(self, state, *args):
        if (
            state
            and not self.is_play_button_pressed()
            or not state
            and self.is_play_button_pressed()
        ):
            with block_signal([self.play_button]):
                self.play_button.toggle()

    def release_all(self, ignore: Optional[Set[QPushButton]] = None):
        for test_button in [
            self.key_step_button,
            self.chord_step_button,
            self.play_button,
        ]:
            if not ignore or test_button not in ignore and test_button.pressed:
                with block_signal([test_button]):
                    test_button.release()

    def stop(self):
        logger.info("stop")

        self.release_all(ignore={self.key_step_button, self.chord_step_button})

        self.manager.sequencer.grid_stop.emit()

    def release_play(self):
        logger.info("stop")

        self.release_all(ignore={self.key_step_button, self.chord_step_button})
