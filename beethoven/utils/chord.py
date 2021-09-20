from dataclasses import replace

from beethoven.objects import Chord


def add_octave_to_chord(chord: Chord, octave: int) -> Chord:
    chord = replace(chord, root=replace(chord.root, octave=octave))
    chord_str = chord.serialize()

    return Chord.parse(chord_str)
