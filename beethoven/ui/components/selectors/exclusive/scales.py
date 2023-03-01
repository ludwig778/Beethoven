from beethoven.ui.components.selectors.exclusive.base import BaseExclusiveSelector
from beethoven.ui.constants import SCALE_LABELS, SCALES_DATA, SELECTED_SCALE, SELECTED_SCALE_LABELS


class ScaleExclusiveSelector(BaseExclusiveSelector):
    def __init__(self, *args, **kwargs):
        super(ScaleExclusiveSelector, self).__init__(
            *args,
            data=SCALES_DATA,
            labels=SCALE_LABELS,
            expanded_labels=SELECTED_SCALE_LABELS,
            checked=SELECTED_SCALE,
            **kwargs
        )
