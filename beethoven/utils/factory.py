from typing import List

from beethoven import factories
from beethoven.core.abstract import AbstractObject
from beethoven.serializers import deserialize


def factory(obj_name: str, string: str, **kwargs: dict) -> AbstractObject:
    parsed = deserialize(obj_name, string)
    obj = getattr(factories, "build_" + obj_name)(parsed, **kwargs)

    return obj


def list_factory(obj_name: str, string: str) -> List[AbstractObject]:
    return [
        factory(obj_name, sub_string)
        for sub_string in string.split(",")
    ]
