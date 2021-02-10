def _get_standard_mapping():
    mapping = []
    note_indexes = [
        (0,  "C", "Do"),
        (2,  "D", "Ré"),
        (4,  "E", "Mi"),
        (5,  "F", "Fa"),
        (7,  "G", "Sol"),
        (9,  "A", "La"),
        (11, "B", "Si")
    ]

    for octave in range(11):
        for note_index, *note_names in note_indexes:
            index = (octave * 12) + note_index + 24

            if index > 127:
                break

            mapping.append([index, octave, *note_names])

    return mapping


standard_midi_mapping = _get_standard_mapping()
