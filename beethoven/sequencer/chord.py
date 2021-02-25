from beethoven.sequencer.note import Note
from beethoven.theory.chord import Chord as BaseChord
from beethoven.theory.chord import ChordSingletonMeta
from beethoven.theory.interval import OCTAVE
from beethoven.utils.regex import SEQUENCER_CHORD_PARSER


class SequencerChordSingletonMeta(ChordSingletonMeta):
    _INSTANCES = {}

    def __call__(cls, root_note=None, chord_name=None, inversion=None, base_note=None):
        if root_note is None and chord_name is None:
            raise ValueError("Chord name and root note must be set")

        elif base_note and not isinstance(base_note, Note):
            base_note = Note(base_note)

        args = frozenset([root_note, chord_name, inversion, base_note])
        if args not in cls._INSTANCES:
            instance = super().__call__(root_note, chord_name, inversion, base_note)
            cls._INSTANCES[args] = instance

        return cls._INSTANCES[args]


class Chord(BaseChord, metaclass=SequencerChordSingletonMeta):
    def __init__(self, root, name, inversion, base_note):
        self._load_attributes(root, name, inversion, base_note)

    def _load_attributes(self, root_note, chord_name, inversion, base_note):
        if not isinstance(root_note, Note):
            root_note = Note(root_note)

        if not (data := self._DIRECTORY.get(chord_name)):
            raise ValueError("Chord name does not exists")

        self.root = root_note
        self.inversion = inversion or 0
        self.base_note = None

        if base_note and base_note != root_note:
            self.base_note = Note.cast_from_theory(
                base_note,
                octave=(
                    self.root.octave
                    if (
                        base_note < self.root or
                        self.root.octave == 0
                    )
                    else self.root.octave - 1
                )
            )

        self.name, self.intervals = data

        if inversion and (inversion < 0 or inversion >= len(self.intervals)):
            raise ValueError("Chord inversion out of range")

        notes = []
        if self.base_note:
            notes.append(self.base_note)

        base_chord_notes = [self.root] + [
            self.root + interval
            for interval in self.intervals[1:]
        ]
        notes += base_chord_notes[self.inversion:] + base_chord_notes[:self.inversion]

        self.notes = [notes[0]]
        last_note = notes[0]
        for note in notes[1:]:
            # AU CAS OU IL Y AURAIT DES INTERVALES ETENDUS
            while note < last_note:
                note += OCTAVE
            self.notes.append(note)
            last_note = note

    @classmethod
    def get_from_fullname(cls, name, **kwargs):
        matched = SEQUENCER_CHORD_PARSER.match(name)
        if not matched:
            return

        parsed = matched.groupdict()

        note_name = parsed.get("note_name")
        alteration = parsed.get("alteration")
        octave = parsed.get("octave")
        chord_name = parsed.get("chord_name")

        return Chord(note_name + alteration + octave, chord_name, **kwargs)
