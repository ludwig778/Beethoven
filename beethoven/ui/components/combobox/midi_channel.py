from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox

# from beethoven.ui.utils import set_object_name
from beethoven.ui.utils import block_signal


class MidiChannelComboBox(QComboBox):
    value_changed = Signal(int)

    def __init__(self, *args, midi_channel: int, **kwargs):
        super(MidiChannelComboBox, self).__init__(*args, **kwargs)

        self.addItems([str(i) for i in range(16)])

        self.set(midi_channel)

        self.currentIndexChanged.connect(self.handle_midi_channel_change)

    def set(self, midi_channel: int):
        self.value = midi_channel

        with block_signal([self]):
            self.setCurrentIndex(midi_channel)

    def handle_midi_channel_change(self, index):
        self.value = index

        self.value_changed.emit(index)
