import logging

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QDialog, QLabel

from beethoven.ui.components.buttons import Button
from beethoven.ui.components.combobox import TuningComboBox
from beethoven.ui.components.selectors import StringSelector
from beethoven.ui.components.spinbox import StringNumberSpinBox
from beethoven.ui.dialogs.tuning_save import TuningSaveDialog
from beethoven.ui.layouts import Spacing, Stretch, horizontal_layout, vertical_layout
from beethoven.ui.managers.app import AppManager
from beethoven.ui.utils import block_signal

logger = logging.getLogger("dialog.tuning")


class TuningDialog(QDialog):
    configuration_changed = Signal()

    def __init__(self, *args, manager: AppManager, **kwargs):
        super(TuningDialog, self).__init__(*args, **kwargs)

        self.setAttribute(Qt.WA_StyledBackground)

        self.tuning_settings = manager.settings.tuning

        self.tuning_selector = TuningComboBox(tuning_settings=self.tuning_settings)
        self.current_tuning = self.tuning_settings.defaults[self.tuning_selector.value]

        self.string_spinbox = StringNumberSpinBox(string_number=len(self.current_tuning.notes))
        self.string_selectors = StringSelector(initial_tuning=self.current_tuning)
        self.ok_button = Button("OK", object_name="blue")
        self.save_button = Button("Save", object_name="green")
        self.delete_button = Button("Delete", object_name="red")

        self.ok_button.clicked.connect(self.close)
        self.save_button.clicked.connect(self.save_tuning)
        self.delete_button.clicked.connect(self.delete_tuning)

        self.tuning_selector.value_changed.connect(self.handle_tuning_name_change)
        self.string_spinbox.value_changed.connect(self.handle_string_number_change)

        self.update_delete_button_state()

        self.setLayout(
            vertical_layout(
                [
                    horizontal_layout(
                        [
                            Stretch(),
                            self.tuning_selector,
                            Stretch(),
                        ]
                    ),
                    Spacing(size=8),
                    horizontal_layout(
                        [
                            Stretch(),
                            QLabel("String number :"),
                            Spacing(size=10),
                            self.string_spinbox,
                            Stretch(),
                        ]
                    ),
                    Spacing(size=12),
                    self.string_selectors,
                    Stretch(),
                    horizontal_layout(
                        [
                            self.ok_button,
                            self.save_button,
                            self.delete_button,
                        ]
                    ),
                ],
                margins=(10, 10, 10, 10),
            )
        )

    def save_tuning(self):
        logger.debug("saving tuning...")

        dialog = TuningSaveDialog(tuning_settings=self.tuning_settings)

        ok, tuning_name = dialog.getText()

        if not ok:
            logger.warning("saving tuning aborted")

            return

        current_tuning = self.string_selectors.value

        logger.info(f"saving tuning: {tuning_name} => {current_tuning.dict()}")

        self.tuning_settings.user_defined[tuning_name] = current_tuning

        self.configuration_changed.emit()

        self.tuning_selector.add(tuning_name)
        self.tuning_selector.set(tuning_name)

        self.update_delete_button_state()

    def delete_tuning(self):
        tuning_name = self.tuning_selector.value

        logger.info(f"deleting tuning: {tuning_name}")

        del self.tuning_settings.user_defined[tuning_name]

        self.tuning_selector.delete_current()

    def handle_string_number_change(self, string_number):
        logger.info(f"update tuning string count to {string_number}")

        self.string_selectors.update_string_number(string_number)

    def handle_tuning_name_change(self, tuning_name):
        logger.info(f"update tuning setting to {tuning_name}")

        tuning = self.tuning_settings.tunings[tuning_name]

        self.current_tuning = tuning

        with block_signal([self.string_spinbox, self.string_selectors]):
            self.string_spinbox.setValue(len(tuning.notes))
            self.string_selectors.set(tuning)

        self.update_delete_button_state()

    def update_delete_button_state(self):
        is_default_tuning = self.tuning_selector.value not in self.tuning_settings.defaults

        if self.delete_button.isEnabled() != is_default_tuning:
            logger.debug(f"update tuning delete button {'active' if is_default_tuning else 'inactive'}")

            return self.delete_button.setEnabled(is_default_tuning)
