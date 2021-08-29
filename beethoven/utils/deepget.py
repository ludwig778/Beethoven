from typing import Any, List, Union


def deepget(data: Any, path: Union[str, List[str]], default: Any = None) -> Any:
    if isinstance(path, str):
        path = path.split(".")

    for item in path:
        if isinstance(data, dict) and item in data:
            data = data.get(item)
        elif isinstance(data, (list, tuple)) and item.isdigit() and 0 < int(item) < len(data):
            data = data[int(item)]
        else:
            return default

    return data
