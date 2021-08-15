from pyparsing import Token


def parse(pattern: Token, string: str, end: bool = False) -> dict:
    data = pattern.parseString(string, parseAll=True)

    return data.asDict()
