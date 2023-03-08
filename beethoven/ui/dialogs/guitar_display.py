import logging

from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QDialog, QLabel, QSizePolicy

from beethoven.models import ChordItem, HarmonyItem
from beethoven.ui.components.buttons import PushPullButton
from beethoven.ui.components.combobox.tuning import TuningComboBox
from beethoven.ui.components.guitar_display import GuitarDisplay
from beethoven.ui.dialogs.tuning import TuningDialog
from beethoven.ui.layouts import Stretch, horizontal_layout, vertical_layout
from beethoven.ui.managers.app import AppManager
from beethoven.ui.utils import block_signal

logger = logging.getLogger("dialog.display_guitar")


class GuitarDisplayDialog(QDialog):
    def __init__(
        self, *args, manager: AppManager, harmony_item: HarmonyItem, chord_item: ChordItem, **kwargs
    ):
        super(GuitarDisplayDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("Guitar Display")

        self.tuning_settings = manager.settings.tuning

        self.graphic = GuitarDisplay(
            tuning=self.tuning_settings.defaults["E Standard"],
            harmony_item=harmony_item,
            chord_item=chord_item,
        )

        self.tuning_combobox = TuningComboBox(tuning_settings=self.tuning_settings)
        self.tuning_combobox.value_changed.connect(self.handle_tuning_name_change)

        self.tuning_dialog = TuningDialog(manager=manager)
        self.tuning_dialog.configuration_changed.connect(self.handle_tuning_configuration_changed)
        self.tuning_dialog_button = PushPullButton("Tuning Settings")
        self.tuning_dialog_button.connect_to_dialog(self.tuning_dialog)

        self.graphic.updated.connect(self.adjustSize)

        self.action_binding = QShortcut(QKeySequence("q"), self)
        self.action_binding.activated.connect(self.close)  # type: ignore

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.update_items = self.graphic.update_items

        self.setLayout(
            vertical_layout(
                [
                    horizontal_layout(
                        [
                            QLabel("Tuning :"),
                            self.tuning_combobox,
                            self.tuning_dialog_button,
                            Stretch(),
                        ]
                    ),
                    self.graphic,
                    Stretch(),
                ],
                margins=(5,) * 4,
            )
        )

    def handle_graphic_resize(self):
        print("handle_graphic_resize")
        self.adjustSize()

    def handle_tuning_configuration_changed(self):
        with block_signal([self.tuning_combobox]):
            self.tuning_combobox.refresh()

        if self.tuning_combobox.value in self.tuning_settings.tunings:
            tuning = self.tuning_settings.tunings[self.tuning_combobox.value]

            if tuning != self.graphic.tuning:
                self.graphic.update_tuning(tuning)
        else:
            self.graphic.update_tuning(self.tuning_settings.tunings[self.tuning_combobox.value])

    def handle_tuning_name_change(self, tuning_name):
        logger.info(f"update tuning setting to {tuning_name}")

        tuning = self.tuning_settings.tunings[tuning_name]

        self.current_tuning = tuning

        self.graphic.update_tuning(tuning)
