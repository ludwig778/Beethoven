from typing import Any, Dict, Generator, Tuple

from beethoven.models import Duration

NoteGenerator = Generator[Tuple[Duration, Any], None, None]
NoteGenerators = Dict[str, NoteGenerator]


def sort_generator_outputs(generators: NoteGenerators) -> NoteGenerator:
    values: Dict[str, Any] = {}

    for name, generator in generators.items():
        try:
            values[name] = next(generator)
        except StopIteration:
            pass

    while values:
        name, item = sorted(values.items(), key=lambda x: x[1][0])[0]

        yield item

        try:
            values[name] = next(generators[name])
        except StopIteration:
            del values[name]
