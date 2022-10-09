from typing import Dict

from beethoven.parsers import patterns


def parse_model_string(model_name: str, string: str) -> Dict:
    pattern = getattr(patterns, f"{model_name}_pattern")

    return pattern.parseString(string, parseAll=True).asDict()
