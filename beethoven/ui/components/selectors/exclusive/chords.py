from beethoven.ui.components.selectors.exclusive.base import ExclusiveSelector
from beethoven.ui.constants import (
    CHORD_LABELS,
    CHORDS_DATA,
    SELECTED_CHORD,
    SELECTED_CHORD_LABELS,
)


class ExclusiveChordSelector(ExclusiveSelector):
    def __init__(self, *args, **kwargs):
        super(ExclusiveChordSelector, self).__init__(
            *args,
            data=CHORDS_DATA,
            labels=CHORD_LABELS,
            expanded_labels=SELECTED_CHORD_LABELS,
            checked=SELECTED_CHORD,
            **kwargs
        )
