from collections import defaultdict


class NameContainer:
    _SETTINGS = defaultdict(int)

    def __init__(self, names):
        self.names = names

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.names[self._SETTINGS[self.__class__.__name__]]

    @classmethod
    def set(cls, index):
        cls._SETTINGS[cls.__name__] = index

    @classmethod
    def get_index(cls):
        return cls._SETTINGS[cls.__name__]
