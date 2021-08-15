from beethoven.objects import Scale


def check_if_diatonic(scale: Scale) -> None:
    if len(scale.notes) != 7:
        raise Exception("You can only get chords from a diatonic scale")
