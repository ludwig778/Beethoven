# from copy import copy
# from typing import Sequence

# from beethoven.helpers.sequencer import note_sequencer
from itertools import cycle
from beethoven.helpers.sequencer import NoteSorter, note_repeater, note_sequencer, one_time_play
from beethoven.models import Duration, Interval, Note
from beethoven.sequencer.objects import BasePlayer, Mapping, PercussionPlayer, Part

# NoteStrategy
#  , Sections
# , Buffer, NoteGeneratorProtocol,


whole = Duration.parse("4")
half = Duration.parse("2")
quarter = Duration.parse("1")
quarter_triplet = Duration.parse("1/3Q")
eighth = Duration.parse("1/2")
sixteenth = Duration.parse("1/4")


class Metronome(PercussionPlayer):
    instrument = "Metronome"

    MAIN_TICK = "Main Tick"
    SEC_TICK = "Secondary Tick"
    ALT_TICK = "Alternate Tick"

    mapping = Mapping(
        mappings={
            MAIN_TICK: Note.parse("G#2"),
            SEC_TICK: Note.parse("D2"),
            ALT_TICK: Note.parse("D#2"),
        }
    )

    def get_notes(self):
        raise NotImplementedError()


class BasicMetronome(Metronome):
    style = "Basic"

    def play(self):
        return NoteSorter(
            main=note_sequencer(quarter, [self.get_note(self.MAIN_TICK)], "+..."),
            sec=note_sequencer(quarter, [self.get_note(self.SEC_TICK)], ".+++"),
        )


class BasicEighthMetronome(Metronome):
    style = "Basic Eighth"

    def play(self):
        return NoteSorter(
            main=note_sequencer(quarter, [self.get_note(self.MAIN_TICK)], "+..."),
            sec=note_sequencer(quarter, [self.get_note(self.SEC_TICK)], ".+++"),
            alt=note_sequencer(eighth, [self.get_note(self.ALT_TICK)], ".+"),
        )


class Piano(BasePlayer):
    instrument = "Piano"


class BasicChordPiano(Piano):
    style = "Basic Chord"

    def play(self):
        timeline = self.part.start_cursor

        #while 1:
        if 1:
            for note in self.part.chord.notes:
                yield timeline, self.get_message(note, self.part.chord_duration)

            timeline += self.part.chord_duration


class BasicArpeggioPiano(Piano):
    style = "Basic Arpeggio"

    def play(self):
        tonic = self.part.chord.notes[0]
        octave = Interval(name="8")
        tonic_2oct = tonic.add_interval(octave).add_interval(octave)

        notes = self.part.chord.notes
        notes += [note.add_interval(octave) for note in self.part.chord.notes]
        notes.append(tonic_2oct)

        timeline = self.part.start_cursor

        for note in cycle(notes + notes[-2:0:-1]):
            yield timeline, self.get_message(note, whole)

            timeline += quarter


# class Drum(BasePlayer):
class Drum(PercussionPlayer):
    instrument = "Drum"

    KICK = "Kick"
    SNARE = "Snare"
    CLOSED_HH = "Closed HH"
    OPEN_HH = "Open HH"
    HIGH_TOM = "High tom"
    MID_TOM = "Mid tom"
    LOW_TOM = "Low tom"
    FLOOR_TOM = "Floor tom"
    RIDE = "Ride"
    CRASH = "Crash"

    mapping = Mapping(
        mappings={
            KICK: Note.parse("C1"),
            SNARE: Note.parse("D1"),
            CLOSED_HH: Note.parse("F#1"),
            OPEN_HH: Note.parse("A#1"),
            RIDE: Note.parse("C#3"),
            CRASH: Note.parse("D4"),
            HIGH_TOM: Note.parse("B1"),
            MID_TOM: Note.parse("A1"),
            LOW_TOM: Note.parse("G1"),
            FLOOR_TOM: Note.parse("F1"),
        }
    )


class BasicDrum(Drum):
    style = "Basic"

    def play(self):
        yield from NoteSorter(
            kick=note_repeater(whole, [self.get_note(self.KICK)]),
            snare=note_repeater(whole, [self.get_note(self.SNARE)], half),
            hh=note_repeater(quarter, [self.get_note(self.CLOSED_HH)]),
            #crash=note_repeater(self.part.chord_duration, [self.get_note(self.CRASH)]),
            crash=one_time_play(self.part.start_cursor, [self.get_note(self.CRASH)]),
        )


class JazzDrum(Drum):
    style = "Jazz"

    def play(self):
        for cursor, note in NoteSorter(
            kick=note_sequencer(eighth, [self.get_note(self.KICK)], "+......+"),
            snare=note_sequencer(eighth, [self.get_note(self.SNARE)], "..+..+.+"),
            ride=note_sequencer(quarter_triplet, [self.get_note(self.RIDE)], "+.+"),
            close_hh=note_sequencer(quarter_triplet, [self.get_note(self.CLOSED_HH, velocity=44)], "...........+" + "." * 12),
            open_hh=note_sequencer(quarter_triplet, [self.get_note(self.OPEN_HH)], "..........+." + "." * 12),
            low_tom=note_sequencer(quarter_triplet, [self.get_note(self.LOW_TOM)], "." * 12 + "..........+."),
            floor_tom=note_sequencer(quarter_triplet, [self.get_note(self.FLOOR_TOM)], "." * 12 + "...........+"),
        ):
            yield self.part.start_cursor + cursor, note

        return
