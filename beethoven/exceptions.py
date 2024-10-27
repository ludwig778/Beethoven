from beethoven.models import Scale
from beethoven.utils.casing import to_pascal_case


class ScaleIsNotDiatonic(Exception):
    def __init__(self, scale: Scale, message: str = "Scale {} is not diatonic") -> None:
        self.scale = scale
        self.message = message.format(scale.to_log_string())
        super().__init__(self.message)


class ScaleNotSet(Exception):
    def __init__(self, message: str = "Scale is not set") -> None:
        self.message = message
        super().__init__(self.message)


class ChordNameUnknown(Exception):
    def __init__(self, chord_name: str, message: str = "Chord named {chord_name} unknown") -> None:
        self.chord_name = chord_name
        self.message = message.format(chord_name=chord_name)
        super().__init__(self.message)


class ScaleNameUnknown(Exception):
    def __init__(self, scale_name: str, message: str = "Scale named {scale_name} unknown") -> None:
        self.scale_name = scale_name
        self.message = message.format(scale_name=scale_name)
        super().__init__(self.message)


class InversionOutOfRange(Exception):
    def __init__(self, message: str = "Out of range") -> None:
        self.message = message
        super().__init__(self.message)


class ParserNotFound(Exception):
    def __init__(self, obj_name: str, message: str = "Couldn't find parser for {obj_name}") -> None:
        self.obj_name = obj_name
        self.message = message.format(obj_name=to_pascal_case(obj_name))
        super().__init__(self.message)


class CouldNotParse(Exception):
    def __init__(self, string: str, obj_name: str, message: str = "Couldn't parse string='{string}' as {obj_name}") -> None:
        self.string = string
        self.obj_name = obj_name
        self.message = message.format(obj_name=to_pascal_case(obj_name), string=string)
        super().__init__(self.message)


class MixedAlteration(Exception):
    pass


class BeatUnitIsInvalid(Exception):
    def __init__(self, beat_unit: int, message: str = "Beat unit {beat_unit} is invalid") -> None:
        self.beat_unit = beat_unit
        self.message = message.format(beat_unit=beat_unit)
        super().__init__(self.message)


class BeatsPerBarCantBeZero(Exception):
    def __init__(self, beats_per_bar: int, message: str = "Beats per bar {beats_per_bar} can't be equal to 0") -> None:
        self.beats_per_bar = beats_per_bar
        self.message = message.format(beats_per_bar=beats_per_bar)
        super().__init__(self.message)


class BpmCantBeZero(Exception):
    def __init__(self, message: str = "Value can't be equal to 0") -> None:
        self.message = message
        super().__init__(self.message)
