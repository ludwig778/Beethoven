from PySide6.QtWidgets import QComboBox

from beethoven.ui.utils import set_object_name


class MidiChannelComboBox(QComboBox):
    def __init__(self, *args, value: int, **kwargs):
        super(MidiChannelComboBox, self).__init__(*args, **kwargs)

        set_object_name(self, **kwargs)

        for i in range(16):
            self.addItem(str(i))

        self.setCurrentText(str(value))
