from functools import partial
from typing import Callable, Dict, Optional

from beethoven.adapters.midi import Output
from beethoven.models import Duration
from beethoven.objects import sixteenth_duration
from beethoven.sequencer.registry import RegisteredPlayer
from beethoven.ui.exceptions import PlayerStopPlaying


class BasePlayer(RegisteredPlayer):
    time_signature_bound: bool = False

    def __init__(self):
        pass

    def reset(self):
        pass

    def play(self, *args, **kwargs):
        raise NotImplementedError()

    def play_wrapper(self, *args, **kwargs):
        return self.play(*args, **kwargs)

    def setup_midi(self, output: Output, channel: int):
        self.output = output
        self.channel = channel

        return self

    def setup(self, scale, chord, time_signature, start_cursor, end_cursor, start_time_section):
        self.scale = scale
        self.chord = chord

        self.time_signature = time_signature

        self.start_cursor = start_cursor
        self.end_cursor = end_cursor
        self.start_time_section = start_time_section

        return self

    def play_note(
        self, cursor: Duration, note_index: int, duration: Duration, velocity: int = 127
    ) -> Dict:
        if cursor > self.end_cursor:
            raise PlayerStopPlaying()

        if cursor + duration > self.end_cursor:
            duration = self.end_cursor - cursor

        return {
            "player": self,
            "note": note_index,
            "velocity": velocity,
            "duration": duration,
        }

    def play_percussion(
        self, note_index: int, duration: Duration = Duration(), velocity: int = 127
    ) -> Dict:
        return {
            "player": self,
            "note": note_index,
            "velocity": velocity,
            "duration": duration,
        }


class PercussionPlayer(BasePlayer):
    time_signature_bound: bool = True

    def __init__(self, *args, time_signature_bound: bool = False, **kwargs):
        super(PercussionPlayer, self).__init__(*args, **kwargs)

        self._gen = None

        if time_signature_bound:
            self.time_signature_bound = True

    def reset(self):
        self._gen = None

    def play_wrapper(self, *args, **kwargs):
        if not self._gen:
            self._gen = self.play(*args, **kwargs)

        return self._gen


class SystemPlayer(PercussionPlayer):
    def __init__(self, *args, **kwargs):
        super(SystemPlayer, self).__init__(*args, **kwargs)

        self.callable: Callable = self._none_callable

    def _none_callable(self, *args, **kwargs):
        pass

    def system_setup(self, callable: Optional[Callable] = None):
        self.callable = callable or self._none_callable

    def play(self):
        for time_section, cursor in self.time_signature.generate_time_sections(
            sixteenth_duration,
            cursor_offset=self.start_cursor,
            base_time_section=self.start_time_section,
        ):
            yield cursor, partial(self.callable, cursor, time_section, self)
