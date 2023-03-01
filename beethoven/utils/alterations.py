from beethoven.utils.interval import is_interval_perfect


def get_note_alteration_int_from_str(alteration: str) -> int:
    if alteration == "":
        return 0
    elif "#" in alteration:
        return alteration.count("#")
    elif "b" in alteration:
        return -alteration.count("b")

    raise ValueError(f"Error on getting note alteration int from str: {alteration}")


def get_note_alteration_str_from_int(alteration: int) -> str:
    if alteration > 0:
        return "#" * alteration
    elif alteration < 0:
        return "b" * abs(alteration)
    else:
        return ""


def get_interval_alteration_int_from_str(alteration: str, interval: int) -> int:
    if alteration in ("", "M"):
        return 0
    elif "m" == alteration:
        return -1
    elif "a" in alteration:
        return alteration.count("a")
    elif "d" in alteration:
        alteration_count = -alteration.count("d")

        if not is_interval_perfect(interval):
            alteration_count -= 1

        return alteration_count

    raise ValueError(f"Error on getting interval alteration int from str: {interval}{alteration}")


def get_interval_alteration_str_from_int(alteration: int, interval: int) -> str:
    if not alteration:
        return ""
    elif is_interval_perfect(interval):
        if alteration > 0:
            return "a" * alteration
        elif alteration < 0:
            return "d" * abs(alteration)
    else:
        if alteration > 0:
            return "a" * alteration
        elif alteration == -1:
            return "m"
        elif alteration < -1:
            return "d" * abs(alteration + 1)

    raise ValueError(f"Error on getting interval alteration str from int: {interval}{alteration}")


def get_degree_alteration_int_from_str(alteration: str) -> int:
    if alteration == "":
        return 0
    elif "#" in alteration:
        return alteration.count("#")
    elif "b" in alteration:
        return -alteration.count("b")

    raise ValueError(f"Error on getting degree alteration int from str: {alteration}")


def get_degree_alteration_str_from_int(alteration: int) -> str:
    if not alteration:
        return ""
    elif alteration > 0:
        return alteration * "#"
    elif alteration < 0:
        return abs(alteration) * "b"

    raise ValueError(f"Error on getting degree alteration str from int: {alteration}")
