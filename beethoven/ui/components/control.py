from logging import getLogger
from enum import Enum, auto
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPushButton, QWidget

from beethoven.ui.components.buttons import PushPullButton
from beethoven.ui.layouts import horizontal_layout
from beethoven.ui.models import HarmonyItems
from beethoven.ui.utils import block_signal

logger = getLogger("control")


class PlayingType(Enum):
    none = auto()
    step = auto()


class PlayerControlWidget(QWidget):
    play_grid = Signal()
    play_grid_step = Signal()
    stop_grid = Signal()

    def __init__(self, *args, harmony_items: HarmonyItems, playing_type: PlayingType, **kwargs):
        super(PlayerControlWidget, self).__init__(*args, **kwargs)

        self.harmony_items = harmony_items

        self.step_player_button = PushPullButton(
            pressed="Step",
            released="Step",
            state=playing_type == PlayingType.step
        )
        self.play_button = PushPullButton(
            pressed="Play",
            released="Play",
            state=False
        )
        self.stop_button = QPushButton("Stop")

        self.step_player_button.toggled.connect(self.step_play)
        self.play_button.toggled.connect(self.play)
        self.stop_button.clicked.connect(self.stop)

        self.setLayout(
            horizontal_layout([
                self.step_player_button,
                self.play_button,
                self.stop_button,
            ])
        )

    def step_play(self, state):
        logger.info(f"step play: {'pressed' if state else 'released'}")

        if self.play_button.is_pressed:
            with block_signal([self.play_button]):
                self.play_button.release()

            self.stop_grid.emit()

            logger.debug("emit stop")

        if state:
            self.play_grid_step.emit()

            logger.debug("emit play step")

    def play(self, state):
        logger.info(f"play: {'pressed' if state else 'released'}")

        if self.step_player_button.is_pressed:
            with block_signal([self.step_player_button]):
                self.step_player_button.release()

        if state:
            self.play_grid.emit()

            logger.debug("emit play")
        else:
            self.stop_grid.emit()

            logger.debug("emit stop")

    def stop(self):
        logger.info("stop")

        with block_signal([self.step_player_button, self.play_button]):
            self.step_player_button.release()
            self.play_button.release()

        self.stop_grid.emit()
