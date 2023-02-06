from logging import getLogger
from typing import Optional

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QComboBox, QDialog, QLabel, QVBoxLayout, QWidget

from beethoven.sequencer.players.registry import RegisteredPlayer
from beethoven.settings import PlayerSetting
from beethoven.ui.components.buttons import Button, PushPullButton
from beethoven.ui.components.combobox import MidiChannelComboBox, MidiOutputComboBox
from beethoven.ui.layouts import Spacing, Stretch, horizontal_layout, vertical_layout
from beethoven.ui.managers import AppManager
from beethoven.ui.utils import block_signal

logger = getLogger("dialog.players")


class PlayerRow(QWidget):
    deleted = Signal(QObject)

    def __init__(
        self,
        *args,
        manager: AppManager,
        settings: PlayerSetting,
        system_player: bool = False,
        **kwargs,
    ):
        super(PlayerRow, self).__init__(*args, **kwargs)

        self.manager = manager
        self.settings = settings
        self.system_player = system_player

        self.instrument_name_combobox = QComboBox()
        self.instrument_name_combobox.setObjectName("instrument_name")

        self.instrument_style_combobox = QComboBox()
        self.instrument_style_combobox.setObjectName("instrument_style")

        self.output_name_combobox = MidiOutputComboBox(
            value=self.settings.output_name, manager=self.manager
        )
        self.channel_combobox = MidiChannelComboBox(midi_channel=self.settings.channel)

        # self.instrument_combobox.setStyleSheet("width: 70px;")

        self.set_instruments()
        self.set_instrument_styles()

        self.instrument_name_combobox.currentTextChanged.connect(
            self.handle_instrument_name_change
        )
        self.instrument_style_combobox.currentTextChanged.connect(
            self.handle_instrument_style_change
        )
        self.output_name_combobox.currentTextChanged.connect(self.setting_changed)
        self.channel_combobox.currentTextChanged.connect(self.setting_changed)

        widgets = [
            self.instrument_name_combobox,
            Spacing(size=2),
            self.instrument_style_combobox,
            Spacing(size=20),
            self.output_name_combobox,
            Spacing(size=2),
            self.channel_combobox,
        ]

        if not self.system_player:
            self.enable_button = PushPullButton(
                "Enable",
                pressed=self.settings.enabled,
                pressed_text="Enabled",
            )
            self.delete_button = Button("X")

            self.enable_button.setObjectName("enable_button")
            self.delete_button.setObjectName("delete_button")

            self.enable_button.toggled.connect(self.setting_changed)
            self.delete_button.clicked.connect(lambda: self.deleted.emit(self))

            widgets += [
                Stretch(),
                self.enable_button,
                Spacing(size=2),
                self.delete_button,
            ]

        self.setLayout(horizontal_layout(widgets, margins=(0, 2, 0, 2)))  # type: ignore

    def set_instruments(self):
        self.instrument_name_combobox.clear()

        self.instrument_name_combobox.addItem("")

        instrument_names = RegisteredPlayer.get_instrument_names()

        for instrument in instrument_names:
            self.instrument_name_combobox.addItem(instrument)

        if (
            self.settings.instrument_name
            and self.settings.instrument_name in instrument_names
        ):
            self.instrument_name_combobox.setCurrentText(self.settings.instrument_name)

    def set_instrument_styles(self):
        self.instrument_style_combobox.clear()

        if not self.settings.instrument_name:
            self.instrument_style_combobox.addItem("")

            return

        player_style_names = list(
            RegisteredPlayer.get_instrument_styles(self.settings.instrument_name).keys()
        )

        self.instrument_style_combobox.addItems(player_style_names)

        if (
            self.settings.instrument_style
            and self.settings.instrument_style in player_style_names
        ):
            self.instrument_style_combobox.setCurrentText(
                self.settings.instrument_style
            )

    def handle_instrument_name_change(self, name: Optional[str]):
        logger.info(f"instrument name set to {name or 'none'}")

        self.settings.instrument_name = name or None

        with block_signal([self.instrument_style_combobox]):
            self.set_instrument_styles()

        if (
            self.instrument_style_combobox.currentText()
            != self.settings.instrument_style
        ):
            self.settings.instrument_style = (
                self.instrument_style_combobox.currentText() or None
            )

        self.manager.configuration_changed.emit()

    def handle_instrument_style_change(self, name: Optional[str]):
        logger.info(f"instrument style set to {name or 'none'}")

        self.settings.instrument_style = name or None

        self.manager.configuration_changed.emit()

    def setting_changed(self):
        self.settings.instrument_name = (
            self.instrument_name_combobox.currentText() or None
        )
        self.settings.output_name = self.output_name_combobox.currentText() or None
        self.settings.channel = int(self.channel_combobox.currentText())

        if not self.system_player:
            self.settings.enabled = self.enable_button.pressed

        self.manager.configuration_changed.emit()


class PlayerDialog(QDialog):
    player_changed = Signal(PlayerSetting)

    def __init__(self, *args, manager: AppManager, **kwargs):
        super(PlayerDialog, self).__init__(*args, **kwargs)

        self.manager = manager

        self.player_list = QVBoxLayout()

        self.ok_button = Button("OK")
        self.add_button = Button("Add Player")

        instrument_settings_label = QLabel("Instrument settings :")
        instrument_settings_label.setObjectName("settings_label")
        instrument_settings_label2 = QLabel("Instrument settings :")
        instrument_settings_label2.setObjectName("settings_label")

        midi_settings_label = QLabel("Midi settings :")
        midi_settings_label.setObjectName("settings_label")
        midi_settings_label2 = QLabel("Midi settings :")
        midi_settings_label2.setObjectName("settings_label")

        self.ok_button.clicked.connect(self.close)
        self.add_button.clicked.connect(self.add_player)

        # self.setup()
        self.setLayout(
            vertical_layout(
                [
                    horizontal_layout(
                        [
                            Spacing(size=188),
                            instrument_settings_label,
                            Spacing(size=181),
                            midi_settings_label,
                            Stretch(),
                        ]
                    ),
                    horizontal_layout(
                        [
                            QLabel("Preview"),
                            PlayerRow(
                                manager=self.manager,
                                settings=self.manager.settings.player.preview,
                                system_player=True,
                            ),
                        ]
                    ),
                    horizontal_layout(
                        [
                            QLabel("Metronome"),
                            PlayerRow(
                                manager=self.manager,
                                settings=self.manager.settings.player.metronome,
                                system_player=True,
                            ),
                        ]
                    ),
                    Spacing(size=16),
                    QLabel("Players"),
                    Spacing(size=12),
                    horizontal_layout(
                        [
                            Spacing(size=10),
                            instrument_settings_label2,
                            Spacing(size=181),
                            midi_settings_label2,
                            Stretch(),
                        ]
                    ),
                    self.player_list,
                    Stretch(),
                    horizontal_layout(
                        [
                            Stretch(),
                            self.ok_button,
                            Spacing(size=5),
                            self.add_button,
                            Stretch(),
                        ],
                        object_name="button_box",
                    ),
                ],
                margins=(10, 10, 10, 10),
            )
        )

        for player_setting in self.manager.settings.player.players:
            self.set_player(player_setting)

    def add_player(self, player_setting: Optional[PlayerSetting] = None, *args):
        logger.info("add player")

        return self.set_player(player_setting)

    def set_player(self, player_setting: Optional[PlayerSetting] = None, *args):
        if not self.room_for_player():
            return

        if player_setting is None:
            player_setting = PlayerSetting()

            self.manager.settings.player.players.append(player_setting)

        player_row = PlayerRow(
            manager=self.manager,
            settings=player_setting,
        )
        player_row.deleted.connect(self.delete_player)

        self.player_list.addWidget(player_row)

        self.update_add_button()

    def room_for_player(self):
        return self.player_list.count() < self.manager.settings.player.max_players

    def delete_player(self, player_row):
        logger.info("delete player")

        self.manager.settings.player.players.remove(player_row.settings)
        self.manager.configuration_changed.emit()

        self.player_list.removeWidget(player_row)

        player_row.close()

        self.update_add_button()

    def update_add_button(self):
        room_for_player = self.room_for_player()

        if self.add_button.isEnabled() != room_for_player:
            logger.debug(
                f"update player add button {'active' if room_for_player else 'inactive'}"
            )

            self.add_button.setEnabled(room_for_player)
