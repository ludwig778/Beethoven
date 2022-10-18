from beethoven.ui.components.selectors.multiple.base import MultipleSelector
from beethoven.ui.constants import SCALE_LABELS, SCALES_DATA, SELECTED_SCALE_LABELS


class MultipleScaleSelector(MultipleSelector):
    def __init__(self, *args, **kwargs):
        super(MultipleScaleSelector, self).__init__(
            *args,
            data=SCALES_DATA,
            labels=SCALE_LABELS,
            expanded_labels=SELECTED_SCALE_LABELS,
            checked_labels=SELECTED_SCALE_LABELS,
            **kwargs
        )
