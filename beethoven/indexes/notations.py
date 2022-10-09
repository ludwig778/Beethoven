from enum import Enum, auto


class NoteNotationEnum(Enum):
    ALPHABETIC = auto()
    SYLLABIC = auto()


class IntervalNotationEnum(Enum):
    SHORT = auto()
    LONG = auto()


class ChordNotationEnum(Enum):
    SHORT = auto()
    FULL = auto()
    SYMBOL = auto()


class ScaleNotationEnum(Enum):
    SHORT = auto()
    FULL = auto()
    SYMBOL = auto()
