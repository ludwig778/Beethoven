from typing import List, Protocol


class Mutator(Protocol):
    def run(self):
        ...


class BaseMutator:
    def run(self, timeline, event):
        pass


def apply_mutators(generator, mutators: List[Mutator]):
    pass
    # for
