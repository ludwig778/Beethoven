from beethoven.sequencer.note import Note
from beethoven.theory.chord import Chord as BaseChord


class Chord(BaseChord):
    def __init__(self, root, name):
        self._load_attributes(root, name)

    def _load_attributes(self, root_note, chord_name):
        if not isinstance(root_note, Note):
            root_note = Note(root_note)

        self.root = root_note

        if not (data := self._DIRECTORY.get(chord_name)):
            raise ValueError("Chord name does not exists")

        self.name, self.intervals = data

        self.notes = [self.root] + [
            self.root + interval
            for interval in self.intervals[1:]
        ]
