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
