from typing import Any


def deepget(data: Any, path: str, default: Any = None) -> Any:
    for item in path.split("."):
        if isinstance(data, dict) and item in data:
            data = data.get(item)
        elif isinstance(data, (list, tuple)) and item.isdigit() and 0 < int(item) < len(data):
            data = data[int(item)]
        else:
            return default

    return data
