from fractions import Fraction

from beethoven.models import Duration, TimeSignature


def get_time_signature_duration(time_signature: TimeSignature) -> Duration:
    return Duration(
        value=Fraction(time_signature.beats_per_bar * 4, time_signature.beat_unit)
    )
