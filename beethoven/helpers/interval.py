def is_interval_perfect(interval: int) -> bool:
    within_octave_interval = ((int(interval) - 1) % 7) + 1

    return within_octave_interval in (1, 4, 5)


def interval_alteration_to_int(alteration: str, interval: int) -> int:
    if alteration in ("", "M"):
        return 0
    if "m" == alteration:
        return -1
    elif "a" in alteration:
        return alteration.count("a")
    elif "d" in alteration:
        alteration_count = -alteration.count("d")

        if not is_interval_perfect(interval):
            alteration_count -= 1

        return alteration_count

    raise ValueError(f"Error on getting int from interval: {interval}{alteration}")
