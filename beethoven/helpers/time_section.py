from fractions import Fraction
from typing import Generator, Tuple

from beethoven.models import Duration, TimeSection, TimeSignature


def time_section_generator(
    ts: TimeSignature, step: Duration
) -> Generator[Tuple[TimeSection, Duration], None, None]:
    cursor = Duration(value=Fraction(0))
    reduction = Fraction(ts.beat_unit, 4)

    bar = measure = 0
    rest = Fraction(0)

    while True:
        yield TimeSection(bar=bar + 1, measure=measure + 1, rest=rest), cursor

        cursor += step

        bar, measure_rest = divmod(cursor.value * reduction, ts.beats_per_bar)
        measure, rest = divmod(measure_rest * reduction, 1)
