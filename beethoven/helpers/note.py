from beethoven.indexes import interval_index, note_index
from beethoven.models import Interval, Note


def note_alteration_to_int(alteration: str) -> int:
    if "#" in alteration:
        return alteration.count("#")
    elif "b" in alteration:
        return -alteration.count("b")
    if "a" in alteration:
        return alteration.count("a")
    elif "d" in alteration:
        return -alteration.count("d")

    return 0


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
