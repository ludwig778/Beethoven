from beethoven.helpers.parsers import parse_model_string
from beethoven.models import TimeSignature


class TimeSignatureController:
    @classmethod
    def parse(cls, string: str) -> TimeSignature:
        parsed = parse_model_string("time_signature", string)

        return cls.constuct(parsed)

    @classmethod
    def constuct(cls, parsed: dict) -> TimeSignature:
        return TimeSignature(
            beats_per_bar=parsed["beats_per_bar"], beat_unit=parsed["beat_unit"]
        )
