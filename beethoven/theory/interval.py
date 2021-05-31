from copy import copy

from beethoven.theory.mappings import interval_mappings
from beethoven.utils.name_container import NameContainer
from beethoven.utils.regex import INTERVAL_PARSER


class IntervalNameContainer(NameContainer):
    @property
    def numeric(self):
        return self.names[0]


class IntervalSingletonMeta(type):
    _INSTANCES = {}

    def __call__(cls, interval_name=None):
        if interval_name is None:
            raise ValueError("Interval name must be set")

        elif interval_name not in cls._INSTANCES:
            instance = super().__call__(interval_name)
            cls._INSTANCES[interval_name] = instance

        return copy(cls._INSTANCES[interval_name])


class Interval(metaclass=IntervalSingletonMeta):
    _DIRECTORY = {}
    _SYSTEM_DIRECTORY = {}
    _REVERSE_DIRECTORY = {}

    def __init__(self, interval_name):
        self._load_attributes(interval_name)

    @property
    def shortname(self):
        return f"{self.name}{self.get_alteration_symbols()}"

    @property
    def fullname(self):
        return f"{self.get_alteration_symbols(fullname=True) or ''} {self.name}".strip()

    def __repr__(self):
        fullname_enabled = IntervalNameContainer.get_index() == 1

        return f"<Interval {self.fullname if fullname_enabled else self.shortname}>"

    def __hash__(self):
        return id(self.system_name)

    def __eq__(self, other):
        return (
            self.index == other.index and
            self.alteration == other.alteration
        )

    def __lt__(self, other):
        return (
            self.index + self.alteration < other.index + other.alteration
        )

    def __le__(self, other):
        return (
            self < other or
            self == other
            # self.index + self.alteration <= other.index + other.alteration
        )

    def get_alteration_symbols(self, **kwargs):
        index = ((int(self.name.numeric) - 1) % 7) + 1
        return self._get_alteration_symbols(index, self.alteration, **kwargs)

    @classmethod
    def _get_alteration_symbols(cls, index, alteration, fullname=False):
        return (
            cls._get_full_alteration_symbols
            if fullname
            else cls._get_short_alteration_symbols
        )(index, alteration)

    @staticmethod
    def _get_short_alteration_symbols(index, alteration):
        if not alteration:
            return ""
        elif alteration > 0:
            return "a" * alteration
        elif index in (2, 3, 6, 7):
            if alteration == -1:
                return "m"
            elif alteration < -1:
                return "d" * (abs(alteration) - 1)
        elif alteration < 0:
            return "d" * abs(alteration)

    @staticmethod
    def _get_full_alteration_symbols(index, alteration):
        if not alteration:
            if index in (2, 3, 6, 7):
                return "major"
            if index in (4, 5):
                return "perfect"
        elif alteration > 0:
            return " ".join(["augmented"] * alteration)
        elif index in (2, 3, 6, 7):
            if alteration == -1:
                return "minor"
            elif alteration < -1:
                return " ".join(["diminished"] * (abs(alteration) - 1))
        elif index in (4, 5) and alteration < 0:
            return " ".join(["diminished"] * abs(alteration))

    @classmethod
    def load(cls, mappings):
        for i, mapping in enumerate(mappings):
            index, *names = mapping
            names_instance = IntervalNameContainer(names)

            for name in names:
                cls._DIRECTORY[name] = (names_instance, index)

            cls._SYSTEM_DIRECTORY[i] = index
            cls._REVERSE_DIRECTORY[index] = i

    @classmethod
    def get_interval_semitones(cls, index):
        return cls._SYSTEM_DIRECTORY[index]

    @classmethod
    def get_interval_degree(cls, index):
        return cls._REVERSE_DIRECTORY[index]

    def _load_attributes(self, interval_name):  # noqa: C901
        parsed = INTERVAL_PARSER.match(interval_name).groupdict()

        interval_name = parsed.get("interval_name")
        alteration_str = parsed.get("alteration")

        alteration_check = []
        if major := "M" in alteration_str:
            alteration_check.append("M")
        if minor := "m" in alteration_str:
            alteration_check.append("m")
        if diminished_num := alteration_str.count("d"):
            alteration_check.append("d")
        if augmented_num := alteration_str.count("a"):
            alteration_check.append("a")

        if len(alteration_check) > 1:
            raise ValueError(
                f"Interval alteration should be of a single type M, m, a or d, not ({', '.join(alteration_check)})"
            )

        if not (data := self._DIRECTORY.get(interval_name)):
            raise ValueError("Interval name does not exists")

        self.name, self.index = data

        normalized_index = ((int(self.name.numeric) - 1) % 7) + 1
        octaves = ((int(self.name.numeric) - 1) // 7)

        alteration = 0
        if normalized_index in (2, 3, 6, 7):
            if minor:
                alteration = -1
            elif augmented_num:
                alteration = augmented_num
            elif diminished_num:
                alteration = - (1 + diminished_num)
        elif normalized_index in (4, 5):
            if major:
                raise ValueError("Major alteration on perfect interval is not possible")
            if minor:
                raise ValueError("Minor alteration on perfect interval is not possible")

            alteration = augmented_num - diminished_num
        elif normalized_index in (1, 8) and alteration_check:
            if major and normalized_index == 1:
                if octaves == 1:
                    raise ValueError("Major alteration on octave interval is not possible")
                else:
                    raise ValueError("Major alteration on unisson interval is not possible")
            if minor and normalized_index == 1:
                if octaves == 1:
                    raise ValueError("Minor alteration on octave interval is not possible")
                else:
                    raise ValueError("Minor alteration on unisson interval is not possible")

            alteration = augmented_num - diminished_num

        self.alteration = alteration

        self.system_name = str(self.name) + alteration_str

    def to_dict(self):
        return {"interval_name": self.name.numeric}


Interval.load(interval_mappings)

AUGMENTED = Interval("1a")
DIMINISHED = Interval("1d")
OCTAVE = Interval("8")
TWO_OCTAVES = Interval("15")
