from typing import Optional

from beethoven.objects import Scale
from beethoven.utils.intervals import is_perfect_interval_class


def check_if_diatonic(scale: Scale) -> None:
    if len(scale.notes) != 7:
        raise Exception("You can only get chords from a diatonic scale")


def validate_alteration(interval: str, alteration: Optional[str]) -> None:
    is_perfect_interval = is_perfect_interval_class(interval)

    if alteration in ("M", "m") and is_perfect_interval:
        raise Exception("Perfect interval class cannot be major or minor")
