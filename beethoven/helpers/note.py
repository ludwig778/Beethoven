from beethoven.indexes import interval_index, note_index
from beethoven.models import Interval, Note


def add_interval_to_note(
    origin: Note, interval: Interval, reverse: bool = False
) -> Note:
    degree_gap = int(interval.name) - 1
    semitone_gap = interval_index.get_semitones(interval.name) + interval.alteration

    if reverse:
        degree_gap *= -1
        semitone_gap *= -1

    origin_index = note_index.get_index(origin.name)
    octave_gap, target_degree = divmod(degree_gap + origin_index, 7)

    origin_semitones = note_index.get_semitones(origin.name)
    destination_note = note_index.get_name_from_index(target_degree % 7)
    destination_semitones = note_index.get_semitones(destination_note)

    destination_alteration = (
        origin_semitones
        + semitone_gap
        + origin.alteration
        - destination_semitones
        - (12 * octave_gap)
    )

    destination_octave = None
    if origin.octave is not None:
        destination_octave = origin.octave + octave_gap

    return Note(
        name=destination_note,
        alteration=destination_alteration,
        octave=destination_octave,
    )


def get_notes_interval(note1: Note, note2: Note) -> Interval:
    index_1 = note_index.get_index(note1.name)
    index_2 = note_index.get_index(note2.name)
    index_diff = index_2 - index_1

    semitones_1 = note_index.get_semitones(note1.name)
    semitones_2 = note_index.get_semitones(note2.name)

    octave_diff = 0
    if note1.octave and note2.octave:
        semitones_1 += note1.octave * 12
        semitones_2 += note2.octave * 12

        semitones_diff = semitones_2 - semitones_1

        octave_diff = note2.octave - note1.octave

        index_diff += octave_diff * 7
    else:
        semitones_diff = (semitones_2 - semitones_1) % 12
        index_diff %= 7

    name = interval_index.get_name_from_index(index_diff)
    semitones = interval_index.get_semitones(name)
    alteration = semitones_diff - semitones - note1.alteration + note2.alteration

    return Interval(name=name, alteration=alteration)
