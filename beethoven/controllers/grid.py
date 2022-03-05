from beethoven.controllers.bpm import BpmController
from beethoven.controllers.chord import ChordController
from beethoven.controllers.duration import DurationController
from beethoven.controllers.scale import ScaleController
from beethoven.controllers.time_signature import TimeSignatureController
from beethoven.models import Bpm, Grid, GridPart, TimeSignature
from beethoven.utils.parser import parse_model_string

DEFAULT_BPM = Bpm(value=120)
DEFAULT_TIME_SIGNATURE = TimeSignature(beats_per_bar=4, beat_unit=4)
DEFAULT_SCALE = ScaleController.parse("C_major")


class GridController:
    @classmethod
    def parse(cls, string: str) -> Grid:
        parsed = parse_model_string("grid", string)

        return cls.construct(parsed)

    @classmethod
    def construct(cls, parsed: dict) -> Grid:
        parts = []

        bpm = DEFAULT_BPM
        time_signature = DEFAULT_TIME_SIGNATURE
        scale = DEFAULT_SCALE

        for parsed_grid_part in parsed["grid_parts"]:
            if not parsed_grid_part:
                continue

            if parsed_bpm := parsed_grid_part.get("bpm"):
                bpm = BpmController.construct(parsed_bpm)

            if parsed_time_signature := parsed_grid_part.get("time_signature"):
                time_signature = TimeSignatureController.construct(
                    parsed_time_signature
                )

            if parsed_scale := parsed_grid_part.get("scale"):
                scale = ScaleController.construct(parsed_scale)

            parsed_chords = parsed_grid_part.get("chords")

            if not parsed_chords:
                continue

            for parsed_chord in parsed_chords:
                chord = ChordController.construct(parsed_chord, scale=scale)

                duration = None
                if parsed_duration := parsed_chord.get("duration"):
                    duration = DurationController.construct(parsed_duration)

                parts.append(
                    GridPart(
                        bpm=bpm,
                        time_signature=time_signature,
                        scale=scale,
                        chord=chord,
                        duration=duration,
                    )
                )

        return Grid(parts=parts)
