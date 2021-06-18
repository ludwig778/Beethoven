from beethoven.theory.mappings import chord_mappings, scale_mappings


def get_chord_names(transform=None):
    names = set()

    for _, *chord_names in chord_mappings:
        for name in chord_names:
            names.add(name)

    if transform:
        names = set(map(transform, names))

    names = set(filter(lambda x: x, names))

    return names


def get_scale_names(transform=None):
    names = set()

    for _, _, *scale_names in scale_mappings:
        for name in scale_names:
            names.add(name)

    if transform:
        names = set(map(transform, names))

    names = set(filter(lambda x: x, names))

    return names
