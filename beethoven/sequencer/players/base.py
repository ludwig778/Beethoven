from beethoven.sequencer.note import Note


class Players:
    REGISTRY = {}
    INSTANCES = {}

    def __init__(self):
        pass

    def add(self, player):
        channel = self._get_first_available_channel()

        self.INSTANCES[channel] = player

    def all(self):
        return self.INSTANCES

    def items(self):
        return self.INSTANCES.items()

    @classmethod
    def _get_first_available_channel(cls):
        channels_taken = cls.INSTANCES.keys()
        
        for i in range(16):
            if i not in channels_taken:
                return i

        raise Exception("All channels taken by players")

    @classmethod
    def get(cls, player_name, **kwargs):
        return cls.REGISTRY.get(player_name)(**kwargs)

    @classmethod
    def register(cls, name, player):
        cls.REGISTRY[name] = player

    def remove(self):
        pass

    def update(self):
        pass


class PlayerMeta(type):
    def __new__(cls, name, bases, dct):
        obj = super().__new__(cls, name, bases, dct)

        print(obj)
        if name != "BasePlayer":
            Players.register(name, obj)

        return obj


class BasePlayer(metaclass=PlayerMeta):
    DEFAULT_DURATION = None
    def play(self, part, *notes, duration=None, velocity=127):
        if not all(map(lambda x: isinstance(x, Note), notes)):
            notes = self._get_notes(*notes)

        if duration is None:
            duration = self.NOTE_DURATION

        return {
            "part": part,
            "notes": notes,
            "duration": duration,
            "velocity": velocity
        }

    def __repr__(self):
        return f"<Player {self.__class__.__name__}>"

    @classmethod
    def _get_notes(cls, *notes):
        return [
            cls.MAPPING.get(note)
            for note in notes
        ]

    def prepare(self, time_signature=None, tempo=None, duration=None, scale=None, chord=None):
        self.time_signature = time_signature
        self.tempo = tempo
        self.duration = duration or self.DEFAULT_DURATION
        self.scale = scale
        self.chord = chord
