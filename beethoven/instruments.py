from beethoven.models import Duration
from beethoven.sequencer.players.base import BasePlayer, PercussionPlayer


class Metronome(PercussionPlayer):
    instrument = "Metronome"
    style = "Basic"

    def play(self):
        return

    def get_default_style(self):
        return ...

    def get_styles(self):
        return {
            "test_1": ...,
            "test_2": ...,
        }


class BasicPiano(BasePlayer):
    instrument = "Piano"
    style = "Basic"

    def play(self):
        timeline = Duration(value=0)

        duration = Duration(value=4)

        while True:
            for note in self.grid_part.chord.notes:
                yield timeline, self.play_note(note.midi_index, duration=duration)

            timeline += duration

    def get_default_style(self):
        return ...

    def get_styles(self):
        return {
            "test_1": ...,
            "test_2": ...,
        }


class BasicDrum(PercussionPlayer):
    instrument = "Drum"
    style = "Basic"

    def play(self):
        pass

    def get_default_style(self):
        return ...

    def get_styles(self):
        return {
            "mid_tempo": ...,
            "blast": ...,
        }


class JazzDrum(PercussionPlayer):
    instrument = "Drum"
    style = "Jazz"

    def play(self):
        pass

    def get_default_style(self):
        return ...

    def get_styles(self):
        return {
            "swing": ...,
            "double_swing": ...,
        }


class FusionJazzDrum(JazzDrum):
    instrument = "Drum"
    style = "Fusion Jazz"

    def play(self):
        pass

    def get_styles(self):
        return {"triple_swing": ..., **super().get_styles()}
