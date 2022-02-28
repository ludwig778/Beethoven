def degree_alteration_to_int(alteration: str) -> int:
    if "#" in alteration:
        return alteration.count("#")
    elif "b" in alteration:
        return -alteration.count("b")

    return 0
