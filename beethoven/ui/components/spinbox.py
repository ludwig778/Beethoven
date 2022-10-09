from PySide6.QtWidgets import QSpinBox

from beethoven.ui.utils import set_object_name


class SpinBox(QSpinBox):
    def __init__(self, *args, minimum: int, value: int, maximum: int, **kwargs):
        super(SpinBox, self).__init__(*args, **kwargs)

        set_object_name(self, **kwargs)

        self.setMinimum(minimum)
        self.setValue(value)
        self.setMaximum(maximum)


class StringNumberSpinBox(SpinBox):
    def __init__(self, *args, **kwargs):
        super(StringNumberSpinBox, self).__init__(*args, minimum=4, maximum=8, **kwargs)
