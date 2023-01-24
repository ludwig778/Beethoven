from beethoven.indexes import chord_index, scale_index
from beethoven.constants import duration
from beethoven.models import Bpm, Duration, Note, Degree, Scale, TimeSignature

DEFAULT_MIDI_INPUT = ""
DEFAULT_MIDI_OUTPUT = ""

DEGREES = Degree.parse_list("I,II,III,IV,V,VI,VII")
ROOTS = Note.parse_list("C,Db,D,Eb,E,F,Gb,G,Ab,A,Bb,B")
ROOTS_WITH_SHARPS = Note.parse_list("C,C#,D,D#,E,F,F#,G,G#,A,A#,B")

NOTES_DATA = {
    "normal": Note.parse_list("C,D,E,F,G,A,B"),
    "flats": Note.parse_list("Db,Eb,Gb,Ab,Bb"),
    "sharps": Note.parse_list("C#,D#,F#,G#,A#"),
}
SELECTED_NOTE = "C"
SELECTED_NOTE_LABELS = ["normal", "flats"]
NOTE_LABELS = ["normal", "flats", "sharps"]

CHORDS_DATA = chord_index.get_chords_label_data()
CHORDS_DATA_FLATTEN = chord_index.get_chords_by_label_data()
SELECTED_CHORD = "major 7"
SELECTED_CHORD_LABELS = ["seventh"]
CHORD_LABELS = [
    "triad",
    "seventh",
    "sixth",
    "suspended",
    "alt seventh",
    "power",
    "alt triad",
]

SCALES_DATA = scale_index.get_scales_label_data()
SELECTED_SCALE = "minor"
SELECTED_SCALE_LABELS = ["main"]
SCALE_LABELS = [
    "main",
    "major",
    "melodic minor",
    "harmonic minor",
    "double harmonic minor",
    "pentatonic",
    "alternative",
]

C_MAJOR4 = Scale.parse("C4_major")

DEFAULT_BPM = Bpm.parse("90")
DEFAULT_TIME_SIGNATURE = TimeSignature.parse("4/4")

BASE_DURATIONS = {
    "Whole": Duration(value=duration.whole_value),
    "Half": Duration(value=duration.half_value),
    "Quarter": Duration(value=duration.quarter_value),
    "Eighth": Duration(value=duration.eighth_value),
    "Sixteenth": Duration(value=duration.sixteenth_value),
}
REVERSED_BASE_DURATIONS = {v: k for k, v in BASE_DURATIONS.items()}
