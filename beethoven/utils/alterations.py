from typing import Optional

from beethoven.utils.intervals import is_perfect_interval_class


def get_alteration_from_int(alteration: int) -> str:
    if not alteration:
        return ""
    elif alteration > 0:
        return "#" * alteration
    elif alteration < 0:
        return "b" * abs(alteration)

    raise Exception(f"UNKNOWN CASE {alteration}")


def get_alteration_as_int(alteration: Optional[str]) -> int:
    if not alteration:
        return 0
    elif alteration.count("#") == len(alteration):
        return alteration.count("#")
    elif alteration.count("b") == len(alteration):
        return - alteration.count("b")
    else:
        raise Exception("Mixed alteration")


def get_interval_alteration_from_int(interval: str, alteration: int) -> str:
    is_perfect_interval = is_perfect_interval_class(interval)

    if not alteration:
        return ""
    elif is_perfect_interval:
        if alteration > 0:
            return "a" * alteration
        elif alteration < 0:
            return "d" * alteration
    else:
        if alteration > 0:
            return "a" * alteration
        elif alteration == -1:
            return "m"
        elif alteration < -1:
            return "d" * (alteration + 1)

    raise Exception(f"UNKNOWN CASE {interval} {alteration}")


def get_interval_alteration_as_int(interval: str, alteration: str) -> int:
    is_perfect_interval = is_perfect_interval_class(interval)

    if is_perfect_interval and alteration.lower() == "m":
        raise Exception("LMMAO")
    elif not alteration or alteration == "M":
        return 0
    elif alteration == "m":
        return -1
    elif alteration.count("a") == len(alteration):
        return alteration.count("a")
    elif alteration.count("d") == len(alteration):
        alteration_count = - alteration.count("d")

        if not is_perfect_interval:
            alteration_count -= 1

        return alteration_count

    raise Exception("LMAO")
