from typing import Any


def check_boolean(value: Any) -> bool:
    return isinstance(value, str) and value.lower() in ("true", "1", "yes")
