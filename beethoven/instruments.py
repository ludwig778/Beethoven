from fractions import Fraction

from beethoven.models import Duration, Note
from beethoven.sequencer.players import BasePlayer, PercussionPlayer


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
        cursor = self.start_cursor
        duration = self.end_cursor

        for note in self.chord.notes:
            yield cursor, self.play_note(cursor, note.midi_index, duration=duration)

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
        """
        yield from NoteSorter({
            "kick": note_sequencer(Duration(value=Fraction(1)), ["KICK"], "+..."),
            "snare": note_sequencer(Duration(value=Fraction(1)), ["SNARE"], "..+."),
            "hh": note_sequencer(Duration(value=Fraction(1, 2)), ["HH"], "+"),
        })

        return
        """

        cursor = self.start_cursor

        duration = Duration(value=Fraction(1, 2))

        KICK = Note.parse("C3").midi_index
        SNARE = Note.parse("C#3").midi_index
        HH = Note.parse("F#3").midi_index

        while True:
            yield cursor, self.play_percussion(KICK)
            yield cursor, self.play_percussion(HH)
            cursor += duration

            yield cursor, self.play_percussion(HH)

            cursor += duration

            yield cursor, self.play_percussion(SNARE)
            yield cursor, self.play_percussion(HH)
            cursor += duration
            yield cursor, self.play_percussion(HH)

            cursor += duration

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
