from beethoven import controllers
from beethoven.indexes import chord_index, scale_index

DEFAULT_MIDI_INPUT = ""
DEFAULT_MIDI_OUTPUT = ""

DEGREES = controllers.degree.parse_list("I,II,III,IV,V,VI,VII")
ROOTS = controllers.note.parse_list("C,Db,D,Eb,E,F,Gb,G,Ab,A,Bb,B")
ROOTS_WITH_SHARPS = controllers.note.parse_list("C,C#,D,D#,E,F,F#,G,G#,A,A#,B")

NOTES_DATA = {
    "normal": controllers.note.parse_list("C,D,E,F,G,A,B"),
    "flats": controllers.note.parse_list("Db,Eb,Gb,Ab,Bb"),
    "sharps": controllers.note.parse_list("C#,D#,F#,G#,A#"),
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

C_MAJOR4 = controllers.scale.parse("C4_major")
