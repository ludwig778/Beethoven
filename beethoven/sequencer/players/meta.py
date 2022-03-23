from __future__ import annotations

from typing import Dict


class PlayerRegistry(type):
    registry: Dict[str, PlayerRegistry] = {}

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)

        if name != "BasePlayer":
            cls.registry[new_cls.__name__] = new_cls

        return new_cls

    @classmethod
    def get_registry(cls):
        return dict(cls.registry)
