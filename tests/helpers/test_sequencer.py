from beethoven.helpers.sequencer import sort_generator_outputs
from beethoven.models import Duration


def test_sequencer_helper_sort_generator_outputs():
    def setup_generator(outputs):
        for output in outputs:
            yield output

    generators = {
        "kick": setup_generator(
            [
                (Duration(value=0), 0),
                (Duration(value=1), 0),
            ]
        ),
        "snare": setup_generator(
            [
                (Duration(value=2), 1),
            ]
        ),
        "hh": setup_generator(
            [
                (Duration(value=0), 2),
                (Duration(value=1), 2),
                (Duration(value=2), 2),
                (Duration(value=3), 2),
            ]
        ),
        "crash": setup_generator([]),
    }

    assert list(sort_generator_outputs(generators)) == [
        (Duration(value=0), 0),
        (Duration(value=0), 2),
        (Duration(value=1), 0),
        (Duration(value=1), 2),
        (Duration(value=2), 1),
        (Duration(value=2), 2),
        (Duration(value=3), 2),
    ]
