import logging

from PySide6.QtWidgets import QPushButton, QWidget

from beethoven.ui.components.buttons import Button, PushPullButton
from beethoven.ui.layouts import horizontal_layout, vertical_layout
from beethoven.ui.utils import block_signal

logger = logging.getLogger("control")


class SequencerWidget(QWidget):
    def __init__(self, *args, manager, **kwargs):
        super(SequencerWidget, self).__init__(*args, **kwargs)

        self.sequencer_manager = manager.sequencer_manager

        self.key_step_button = PushPullButton("Key Step", object_name="key_step")
        self.chord_step_button = PushPullButton("Chord Step", object_name="chord_step")
        self.play_button = PushPullButton("Play", object_name="play")
        self.stop_button = Button("Stop", object_name="stop")

        self.key_step_button.toggled.connect(self.handle_key_step)
        self.chord_step_button.toggled.connect(self.handle_chord_step)

        self.play_button.toggled.connect(self.handle_play)
        self.stop_button.clicked.connect(self.handle_stop)

        self.setLayout(
            vertical_layout(
                [
                    self.key_step_button,
                    self.chord_step_button,
                    horizontal_layout([self.play_button, self.stop_button]),
                ]
            )
        )

    def setup(self):
        self.sequencer_manager.grid_play.connect(self.ensure_play_button_pressed)
        self.sequencer_manager.grid_ended.connect(self.release_play_button)
        """
        """

        # self._set_pressed_play_button_func = partial(self.set_play_button_state, True)
        # self._set_release_play_button_func = partial(self.set_play_button_state, False)
        # self.sequencer_manager.grid_play.connect(self._set_pressed_play_button_func)
        # self.sequencer_manager.grid_stop.connect(self._set_release_play_button_func)

    def teardown(self):
        # self.sequencer_manager.grid_play.disconnect(self._set_pressed_play_button_func)
        # self.sequencer_manager.grid_stop.disconnect(self._set_release_play_button_func)

        if not self.sequencer_manager.is_stopped():
            self.sequencer_manager.grid_stop.emit()

        self.sequencer_manager.grid_play.disconnect(self.ensure_play_button_pressed)
        self.sequencer_manager.grid_ended.disconnect(self.release_play_button)
        # self.sequencer_manager.grid_ended.disconnect(self.release_play)

        for btn in (self.play_button, self.key_step_button, self.chord_step_button):
            self.release(btn)

    def handle_key_step(self, state):
        logger.info(f"key step play: {'pressed' if state else 'released'}")
        print(f"SequencerWidget :: key step play: {'pressed' if state else 'released'}")

        self.release(self.chord_step_button)

    def handle_chord_step(self, state):
        logger.info(f"chord step play: {'pressed' if state else 'released'}")
        print(f"SequencerWidget :: chord step play: {'pressed' if state else 'released'}")

        self.release(self.key_step_button)

    def handle_play(self, state):
        logger.info(f"play: {'pressed' if state else 'released'}")
        print(f"SequencerWidget :: play: {'pressed' if state else 'released'}")

        if not state and not self.sequencer_manager.is_stopped():
            # self.sequencer_manager.grid_stop.emit()
            self.sequencer_manager.stop()

            logger.info("stop")
        elif state:
            # self.sequencer_manager.grid_play.emit({"preview": False})
            self.sequencer_manager.play()

            logger.info("play")

    def handle_stop(self):
        logger.info("stop")
        print("SequencerWidget :: stop")

        self.sequencer_manager.stop()
        self.release(self.play_button)
        # self.release_all(ignore={self.key_step_button, self.chord_step_button})

    def release(self, push_button: QPushButton):
        if push_button.pressed:
            with block_signal([push_button]):
                push_button.release()

    def is_play_button_pressed(self):
        return self.play_button.pressed

    def is_key_step_button_pressed(self):
        return self.key_step_button.pressed

    def is_chord_step_button_pressed(self):
        return self.chord_step_button.pressed

    """
    def press_play_button(self):
        if not self.play_button.pressed():
            with block_signal([self.play_button]):
                self.play_button.toggle()

    def release_chord_step_button(self):
        if self.chord_step_button.pressed():
            self.release(self.chord_step_button)

    def release_key_step_button(self):
        if self.key_step_button.pressed():
            self.release(self.key_step_button)
    """

    def ensure_play_button_pressed(self):
        if not self.play_button.pressed:
            with block_signal([self.play_button]):
                self.play_button.toggle()

    def release_play_button(self):
        if self.play_button.pressed:
            self.release(self.play_button)
