from itertools import product
from typing import List

from beethoven import controllers
from beethoven.models import Note


def chord_product(roots: List[Note], chord_names: List[str]):
    return [
        controllers.chord.parse(f"{str(root)}_{chord_name}")
        for root, chord_name in product(roots, chord_names)
    ]
