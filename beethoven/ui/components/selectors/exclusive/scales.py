from beethoven.ui.components.selectors.exclusive.base import ExclusiveSelector
from beethoven.ui.constants import (
    SCALE_LABELS,
    SCALES_DATA,
    SELECTED_SCALE,
    SELECTED_SCALE_LABELS,
)


class ExclusiveScaleSelector(ExclusiveSelector):
    def __init__(self, *args, **kwargs):
        super(ExclusiveScaleSelector, self).__init__(
            *args,
            data=SCALES_DATA,
            labels=SCALE_LABELS,
            expanded_labels=SELECTED_SCALE_LABELS,
            checked=SELECTED_SCALE,
            **kwargs
        )
