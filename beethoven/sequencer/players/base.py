from beethoven.sequencer.note import Note, note_mapping
from beethoven.sequencer.players.arpeggiator import Arpeggiator
from beethoven.sequencer.players.chord_voicer import ChordVoicer


class Players:
    REGISTRY = {}
    MAX_CHANNELS = 16

    def __init__(self, *players):
        self.instances = {}

        for player in players:
            self.add(player)

    def add(self, player):
        channel = self._get_first_available_channel()

        self.instances[channel] = player

    def all(self):
        return self.instances

    def items(self):
        return self.instances.items()

    def _get_first_available_channel(self):
        channels_taken = self.instances.keys()

        for i in range(self.MAX_CHANNELS):
            if i not in channels_taken:
                return i

        raise Exception("All channels taken by players")

    @classmethod
    def get(cls, player_name, **kwargs):
        return cls.REGISTRY.get(player_name)(**kwargs)

    @classmethod
    def register(cls, name, player):
        cls.REGISTRY[name] = player

    def remove(self, index):
        if index in self.instances:
            del self.instances[index]

    def update(self, players_channel):
        self.instances.update(players_channel)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"<Players : {len(self.instances)} players>"


class PlayerMeta(type):
    def __new__(cls, name, bases, dct):
        obj = super().__new__(cls, name, bases, dct)

        if not dct.get("ABSTRACT", False):
            Players.register(name, obj)

        return obj


class BasePlayer(metaclass=PlayerMeta):
    ABSTRACT = True
    DEFAULT_DURATION = None
    NOTE_RANGE = [None, None]
    MAPPING = note_mapping

    def __init__(self):
        self.arpeggiator = Arpeggiator(self)
        self.chord_voicer = ChordVoicer(self)

        self.part = None

    def play(self, *notes, duration=None, velocity=127):
        if notes and not all(map(lambda x: isinstance(x, Note), notes)):
            notes = self._get_notes(*notes)

        if duration is None:
            duration = self.NOTE_DURATION

        return {
            "part": self.part,
            "notes": notes,
            "duration": duration,
            "velocity": velocity
        }

    def check(self, **kwargs):
        if not self.part:
            return False

        if getattr(self, "NORMALIZE_TS", False):
            part = self.time_signature.normalize_part(self.part)
        else:
            part = self.part

        checks = []
        for k, v in kwargs.items():
            part_value = getattr(part, k)
            if isinstance(v, int):
                checks.append(part_value == v)
            else:
                checks.append(part_value in v)

        return all(checks)

    def __repr__(self):
        return f"{str(self)}"

    def __str__(self):
        return f"<Player {self.__class__.__name__}>"

    @classmethod
    def _get_notes(cls, *notes):
        return [
            cls.MAPPING.get(note)
            for note in notes
        ]

    def prepare(self, time_signature=None, tempo=None, duration=None, scale=None, chord=None, **kwargs):
        self.time_signature = time_signature
        self.tempo = tempo
        self.duration = duration or self.DEFAULT_DURATION

        self.scale = scale
        self.chord = chord
