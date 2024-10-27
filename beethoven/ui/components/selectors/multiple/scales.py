from beethoven.ui.components.selectors.multiple.base import \
    BaseMultipleSelector
from beethoven.ui.constants import (SCALE_LABELS, SCALES_DATA,
                                    SELECTED_SCALE_LABELS)


class ScaleMultipleSelector(BaseMultipleSelector):
    def __init__(self, *args, **kwargs):
        super(ScaleMultipleSelector, self).__init__(
            *args,
            data=SCALES_DATA,
            labels=SCALE_LABELS,
            expanded_labels=SELECTED_SCALE_LABELS,
            checked_labels=SELECTED_SCALE_LABELS,
            **kwargs
        )
