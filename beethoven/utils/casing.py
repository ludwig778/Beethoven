def to_pascal_case(string: str) -> str:
    return "".join([n.capitalize() for n in string.split("_")])
