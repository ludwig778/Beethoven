from __future__ import annotations

import logging
from typing import Dict, List

logger = logging.getLogger("players.registry")


class RegisteredPlayerMeta(type):
    instances: Dict[str, Dict[str, RegisteredPlayerMeta]] = {}

    def __new__(cls, clsname, superclasses, attributedict):  # type: ignore[no-untyped-def]
        newclass = type.__new__(cls, clsname, superclasses, attributedict)

        if hasattr(newclass, "instrument") and hasattr(newclass, "style"):
            if newclass.instrument not in cls.instances:
                cls.instances[newclass.instrument] = {}

            cls.instances[newclass.instrument][newclass.style] = newclass

            logger.info(f"registering player: {newclass.instrument} - {newclass.style}")

        return newclass

    @classmethod
    def get_instrument_names(cls) -> List[str]:
        return list(cls.instances.keys())

    @classmethod
    def get_instrument_styles(cls, instrument_name: str) -> Dict[str, RegisteredPlayerMeta]:
        return cls.instances.get(instrument_name, {})

    @classmethod
    def get_instrument_style(cls, instrument_name: str, style_name: str) -> RegisteredPlayerMeta | None:
        return cls.instances.get(instrument_name, {}).get(style_name)


class RegisteredPlayer(metaclass=RegisteredPlayerMeta):
    pass
