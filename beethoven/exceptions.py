from beethoven.utils.casing import to_pascal_case


class ScaleIsNotDiatonic(Exception):
    def __init__(self, scale, message="Scale {} is not diatonic"):
        self.scale = scale
        self.message = message.format(scale.serialize())
        super().__init__(self.message)


class ScaleNotSet(Exception):
    def __init__(self, message="Scale is not set"):
        self.message = message
        super().__init__(self.message)


class ChordNameUnknown(Exception):
    def __init__(self, chord_name, message="Chord named {chord_name} unknown"):
        self.chord_name = chord_name
        self.message = message.format(chord_name=chord_name)
        super().__init__(self.message)


class ScaleNameUnknown(Exception):
    def __init__(self, scale_name, message="Scale named {scale_name} unknown"):
        self.scale_name = scale_name
        self.message = message.format(scale_name=scale_name)
        super().__init__(self.message)


class InversionOutOfRange(Exception):
    def __init__(self, message="Out of range"):
        self.message = message
        super().__init__(self.message)


class ParserNotFound(Exception):
    def __init__(self, obj_name, message="Couldn't find parser for {obj_name}"):
        self.obj_name = obj_name
        self.message = message.format(obj_name=to_pascal_case(obj_name))
        super().__init__(self.message)


class CouldNotParse(Exception):
    def __init__(self, string, obj_name, message="Couldn't parse string='{string}' as {obj_name}"):
        self.string = string
        self.obj_name = obj_name
        self.message = message.format(obj_name=to_pascal_case(obj_name), string=string)
        super().__init__(self.message)


class MixedAlteration(Exception):
    pass


class BeatUnitIsInvalid(Exception):
    def __init__(self, beat_unit, message="Beat unit {beat_unit} is invalid"):
        self.beat_unit = beat_unit
        self.message = message.format(beat_unit=beat_unit)
        super().__init__(self.message)


class BeatsPerBarCantBeZero(Exception):
    def __init__(self, beats_per_bar, message="Beats per bar {beats_per_bar} can't be equal to 0"):
        self.beats_per_bar = beats_per_bar
        self.message = message.format(beats_per_bar=beats_per_bar)
        super().__init__(self.message)


class BpmCantBeZero(Exception):
    def __init__(self, message="Value can't be equal to 0"):
        self.message = message
        super().__init__(self.message)
