from beethoven.ui.components.selectors.exclusive.base import BaseExclusiveSelector
from beethoven.ui.constants import (
    CHORD_LABELS,
    CHORDS_DATA,
    SELECTED_CHORD,
    SELECTED_CHORD_LABELS,
)


class ChordExclusiveSelector(BaseExclusiveSelector):
    def __init__(self, *args, **kwargs):
        super(ChordExclusiveSelector, self).__init__(
            *args,
            data=CHORDS_DATA,
            labels=CHORD_LABELS,
            expanded_labels=SELECTED_CHORD_LABELS,
            checked=SELECTED_CHORD,
            **kwargs
        )
