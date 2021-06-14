def check_boolean(value):
    return isinstance(value, str) and value.lower() in ("true", "1", "yes")
