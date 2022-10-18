from logging import getLogger

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from beethoven.ui.components.combobox import TuningComboBox
from beethoven.ui.components.selectors import StringSelector
from beethoven.ui.components.spinbox import StringNumberSpinBox
from beethoven.ui.dialogs.tuning_save import TuningSaveDialog
from beethoven.ui.settings import TuningSettings
from beethoven.ui.utils import block_signal

logger = getLogger("dialog.tuning")


class TuningDialog(QWidget):
    configuration_changed = Signal()

    def __init__(self, *args, tuning_settings: TuningSettings, **kwargs):
        super(TuningDialog, self).__init__(*args, **kwargs)

        self.tuning_settings = tuning_settings

        self.setup()

    def setup(self):
        logger.debug("setup")

        self.tuning_selector = TuningComboBox(tuning_settings=self.tuning_settings)
        self.current_tuning = self.tuning_selector.current_tuning

        self.string_spinbox = StringNumberSpinBox(value=len(self.current_tuning.notes))
        self.string_selectors = StringSelector(initial_tuning=self.current_tuning)
        self.ok_button = QPushButton("OK")
        self.save_button = QPushButton("Save")
        self.delete_button = QPushButton("Delete")

        self.ok_button.clicked.connect(self.close)
        self.save_button.clicked.connect(self.save_tuning)
        self.delete_button.clicked.connect(self.delete_tuning)

        self.tuning_selector.currentTextChanged.connect(self.update_tuning_setting)
        self.string_spinbox.valueChanged.connect(self.update_string_widgets)

        self.update_delete_button_state()

        self.setLayout(self.get_layout())

    def save_tuning(self):
        logger.debug("saving tuning...")

        dialog = TuningSaveDialog(tuning_settings=self.tuning_settings)

        ok, tuning_name = dialog.getText()

        if not ok:
            logger.warning("saving tuning aborted")

            return

        current_tuning = self.string_selectors.get_tuning()

        logger.info(f"saving tuning: {tuning_name} => {current_tuning.dict()}")

        self.tuning_settings.user_defined[tuning_name] = current_tuning

        self.configuration_changed.emit()

        self.tuning_selector.add_tuning(tuning_name)
        self.tuning_selector.set_tuning(tuning_name)

    def delete_tuning(self):
        tuning_name = self.tuning_selector.current_tuning_name

        logger.info(f"deleting tuning: {tuning_name}")

        del self.tuning_settings.user_defined[tuning_name]

        self.tuning_selector.delete_current_tuning()

    def update_string_widgets(self, string_number):
        logger.info(f"update tuning string count to {string_number}")

        self.string_selectors.update_string_widgets(string_number)

    def update_tuning_setting(self, tuning_name):
        logger.info(f"update tuning setting to {tuning_name}")

        tuning = self.tuning_settings.tunings[tuning_name]

        self.current_tuning = tuning

        with block_signal([self.string_selectors]):
            self.string_spinbox.setValue(len(tuning.notes))
            self.string_selectors.set_tuning(tuning)

        self.update_delete_button_state()

    def update_delete_button_state(self):
        is_default_tuning = (
            self.tuning_selector.current_tuning_name
            not in self.tuning_settings.defaults
        )

        if self.delete_button.isEnabled() != is_default_tuning:
            logger.debug(
                f"update tuning delete button {'active' if is_default_tuning else 'inactive'}"
            )

            return self.delete_button.setEnabled(is_default_tuning)

    def get_layout(self):
        main_layout = QVBoxLayout()

        spinbox_layout = QHBoxLayout()
        spinbox_layout.addWidget(QLabel("Strings :"))
        spinbox_layout.addWidget(self.string_spinbox)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.ok_button)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.delete_button)

        main_layout.addWidget(self.tuning_selector)
        main_layout.addLayout(spinbox_layout)
        main_layout.addWidget(self.string_selectors)

        main_layout.addLayout(buttons_layout)

        return main_layout
