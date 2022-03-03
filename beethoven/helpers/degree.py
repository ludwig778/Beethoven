from beethoven.indexes import degree_index
from beethoven.models import Degree, Interval


def get_interval_from_degree(degree: Degree) -> Interval:
    return Interval(
        name=degree_index.get_index(degree.name) + 1, alteration=degree.alteration
    )
