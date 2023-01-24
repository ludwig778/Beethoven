from enum import Enum, auto
from logging import getLogger
from typing import Optional

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPushButton, QWidget

from beethoven.ui.components.buttons import PushPullButton
from beethoven.ui.layouts import Spacing, horizontal_layout, vertical_layout
from beethoven.ui.utils import block_signal

logger = getLogger("control")


class PlayingType(Enum):
    none = auto()
    step = auto()


class PlayerControl(QWidget):
    play_grid = Signal()
    play_grid_harmony_step = Signal()
    play_grid_chord_step = Signal()
    stop_grid = Signal()

    def __init__(self, *args, **kwargs):
        super(PlayerControl, self).__init__(*args, **kwargs)

        self.key_step_button = PushPullButton("Key Step Mode")
        self.chord_step_button = PushPullButton("Chord Step Mode")
        self.play_button = PushPullButton("Play")
        self.stop_button = QPushButton("Stop")

        self.key_step_button.toggled.connect(self.handle_key_step)
        self.chord_step_button.toggled.connect(self.handle_chord_step)

        self.play_button.toggled.connect(self.play)
        self.stop_button.clicked.connect(self.stop)

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

    def is_key_step_button_pressed(self):
        return self.key_step_button.pressed

    def is_chord_step_button_pressed(self):
        return self.chord_step_button.pressed

    def is_play_button_pressed(self):
        return self.play_button.pressed

    def handle_key_step(self, state):
        logger.info(f"harmony step play: {'pressed' if state else 'released'}")

        if self.is_play_button_pressed() or self.is_key_step_button_pressed():
            self.stop_grid.emit()

            logger.debug("emit stop")

        self.release_all(ignore=self.key_step_button)

        if state:
            self.play_grid_harmony_step.emit()

            logger.debug("emit play harmony step")
        else:
            self.stop_grid.emit()

            logger.debug("emit stop")

    def handle_chord_step(self, state):
        logger.info(f"chord step play: {'pressed' if state else 'released'}")

        if self.is_play_button_pressed() or self.is_key_step_button_pressed():
            self.stop_grid.emit()

            logger.debug("emit stop")

        self.release_all(ignore=self.chord_step_button)

        if state:
            self.play_grid_chord_step.emit()

            logger.debug("emit play chord step")
        else:
            self.stop_grid.emit()

            logger.debug("emit stop")

    def play(self, state):
        logger.info(f"play: {'pressed' if state else 'released'}")

        self.release_all(ignore=self.play_button)

        if self.is_chord_step_button_pressed() or self.is_play_button_pressed():
            self.stop_grid.emit()

            logger.debug("emit stop")

        if state:
            self.play_grid.emit()

            logger.debug("emit play")
        else:
            self.stop_grid.emit()

            logger.debug("emit stop")

    def release_all(self, ignore: Optional[QPushButton] = None):
        for test_button in [
            self.key_step_button,
            self.chord_step_button,
            self.play_button,
        ]:
            if test_button != ignore and test_button.pressed:
                with block_signal([test_button]):
                    test_button.release()

    def stop(self):
        logger.info("stop")

        self.release_all()

        self.stop_grid.emit()
