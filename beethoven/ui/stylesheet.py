from typing import List, Optional

from beethoven.ui.utils import color_from_hsl

WHITE = color_from_hsl(0, 0, 100)
SOFT_GRAY = color_from_hsl(0, 0, 97)
SOFT_GRAY_2 = color_from_hsl(0, 0, 95)
LIGHT_GRAY = color_from_hsl(0, 0, 85)
LIGHT_GRAY_2 = color_from_hsl(0, 0, 76)
MEDIUM_GRAY = color_from_hsl(0, 0, 70)
DARKER_GRAY = color_from_hsl(0, 0, 55)
DARK_GRAY = color_from_hsl(0, 0, 40)
BLACK = color_from_hsl(0, 0, 0)

SOFT_GREEN = color_from_hsl(120, 60, 85)
LIGHT_GREEN = color_from_hsl(120, 60, 70)
GREEN = color_from_hsl(120, 60, 55)
SLIGHTLY_DARKER_GREEN = color_from_hsl(120, 60, 45)
DARKER_GREEN = color_from_hsl(120, 60, 42)

SOFT_BLUE = color_from_hsl(199, 92, 80)
LIGHT_BLUE = color_from_hsl(199, 92, 74)
BLUE = color_from_hsl(199, 92, 62)
SLIGHTLY_DARKER_BLUE = color_from_hsl(199, 92, 47)

SOFT_RED = color_from_hsl(14, 100, 89)
LIGHT_RED = color_from_hsl(14, 100, 78)
RED = color_from_hsl(14, 100, 57)
SLIGHTLY_DARKER_RED = color_from_hsl(14, 100, 50)

SOFT_ORANGE = color_from_hsl(24, 100, 89)
LIGHT_ORANGE = color_from_hsl(24, 100, 78)
ORANGE = color_from_hsl(24, 100, 57)
SLIGHTLY_DARKER_ORANGE = color_from_hsl(24, 100, 50)
DARKER_ORANGE = color_from_hsl(24, 100, 40)

MAIN_WINDOW_GRAY = color_from_hsl(0, 0, 92)
BORDER_COLOR = LIGHT_GRAY_2
BUTTON_BG_COLOR = LIGHT_GRAY

FRAME_UPPER_TEXT = color_from_hsl(0, 0, 53)
FRAME_MAIN_TEXT = color_from_hsl(0, 0, 33)

ERROR_COLOR = RED


def setup_style(styles: dict, path: Optional[List[str]] = None):
    style = ""
    path = path or []

    for key, style_data in styles.items():
        if isinstance(style_data, dict):
            style += setup_style(style_data, path=path + [key])
        else:
            style += "".join(path + [key]) + " {" + style_data + "}\n"

    return style


def get_stylesheet() -> str:
    return setup_style(
        {
            "*": (
                "padding: 0px;"
                "margin:  0px;"
                f"color: {BLACK};"
                # "border: 1px solid red;"
            ),
            "MainWindow": f"min-width: 500px;background-color: {MAIN_WINDOW_GRAY};",
            "QDialog": {
                "": f"background-color: {MAIN_WINDOW_GRAY};",
                " #error_label": f"color: {ERROR_COLOR};font: bold;font-size: 12px;",
            },
            "QListView": f"background-color: {SOFT_GRAY};",
            "QComboBox": {
                " QAbstractItemView": f"selection-background-color: {LIGHT_BLUE};",
            },
            "QSpinBox": f"background-color: {SOFT_GRAY};",
            "QLineEdit": f"background-color: {SOFT_GRAY};",
            "QPushButton": {
                "": f"background-color: {SOFT_GRAY};border: 1px solid {BORDER_COLOR};",
                ":hover": f"background-color: {LIGHT_GRAY};",
                ":pressed": f"background-color: {LIGHT_GRAY_2};",
                ":disabled": f"background-color: {LIGHT_GRAY};color: {DARKER_GRAY};",
                "#blue": {
                    ":hover": f"background-color: {LIGHT_BLUE};",
                    ":pressed": f"background-color: {BLUE};",
                },
                "#green": {
                    ":hover": f"background-color: {LIGHT_GREEN};",
                    ":pressed": f"background-color: {GREEN};",
                },
                "#red": {
                    ":hover": f"background-color: {LIGHT_RED};",
                    ":pressed": f"background-color: {RED};",
                },
            },
            "PushPullButton": {
                "[pressed=true]": f"background-color: {MEDIUM_GRAY};",
                ":hover[pressed=true]": f"background-color: {DARKER_GRAY};",
            },
            "HarmonyTrainerWidget > ": {
                "#step_interval_section > #mode_combobox": "width: 70px;padding-left: 20px;",
            },
            "HarmonyPicker": {
                "": "min-height: 71px;max-height: 71px;",
                " > BpmSpinBox": "min-width: 70px;max-width: 70px;",
            },
            "ComposerGrid QPushButton": {
                "#green": {
                    ":hover": f"background-color: {SOFT_GREEN};",
                    ":pressed": f"background-color: {LIGHT_GREEN};",
                },
                "#red": {
                    ":hover": f"background-color: {SOFT_RED};",
                    ":pressed": f"background-color: {LIGHT_RED};",
                },
                "#blue": {
                    ":hover": f"background-color: {SOFT_BLUE};",
                    ":pressed": f"background-color: {LIGHT_BLUE};",
                    "[pressed=true]": f"background-color: {LIGHT_BLUE};",
                    ":hover[pressed=true]": f"background-color: {BLUE};",
                    ":pressed[pressed=true]": f"background-color: {SLIGHTLY_DARKER_BLUE};",
                },
            },
            "HarmonyGrid": {
                " QListView": f"border: 1px solid {BORDER_COLOR};",
                " > QPushButton": "height: 100%;width: 40px;",
            },
            "ChordGrid": {
                " QListView": f"border: 1px solid {BORDER_COLOR};",
                " > QPushButton": "height: 100%;width: 40px;",
            },
            "ScalePicker > ": {
                "NoteComboBox": "padding-left: 10px;margin-left: -4px;min-width: 50px;max-width: 50px;",
                "ScaleComboBox": "padding-left: 12px;margin-left: -3px;min-width: 100px;max-width: 100px;",
                "OctaveSpinBox": "padding-left: 4px;margin-left: -4px;min-width: 36px;max-width: 36px;",
            },
            "ChordPicker": {
                "": "min-width: 500px;max-width: 500px;",
                " QPushButton": {
                    "": "height: 24px;width: 65px;",
                    "[pressed=true]": f"background-color: {LIGHT_GREEN};",
                },
                " > ": {
                    "DegreeAlterationComboBox": "padding-left: 10px;width: 40px;",
                },
                " DurationSelector > ": {
                    "SpinBox": "padding-left: 10px;width: 50px;",
                    "QComboBox": "padding-left: 15px;width: 80px;",
                },
                " InversionSpinBox": "width: 40px;",
            },
            "FramedText": {
                "": (
                    "min-height: 33px;"
                    "max-height: 33px;"
                    f"background-color: {WHITE};"
                    f"border: 1px solid {BORDER_COLOR};"
                    "border-radius: 5px;"
                ),
                "#upper_text": f"font-size: 8px;font: bold;color: {FRAME_UPPER_TEXT};",
                "#main_text": f"padding-top: 1px;font-size: 18px;font: bold;color: {FRAME_MAIN_TEXT};",
            },
            "SequencerWidget": {
                "": "min-height: 71px;max-height: 71px;min-width: 160px;max-width: 160px;",
                " > QPushButton": {
                    "": "height: 33.6%;",
                    "#key_step": {
                        "": "border-top-left-radius: 5px;border-top-right-radius: 5px;",
                        ":hover": f"background-color: {LIGHT_ORANGE};",
                        "[pressed=true]": f"background-color: {ORANGE};",
                        ":hover[pressed=true]": f"background-color: {SLIGHTLY_DARKER_ORANGE};",
                    },
                    "#chord_step": {
                        ":hover": f"background-color: {LIGHT_BLUE};",
                        "[pressed=true]": f"background-color: {BLUE};",
                        ":hover[pressed=true]": f"background-color: {SLIGHTLY_DARKER_BLUE};",
                    },
                    "#play": {
                        "": "border-bottom-left-radius: 5px;",
                        ":hover": f"background-color: {LIGHT_GREEN};",
                        "[pressed=true]": f"background-color: {GREEN};",
                        ":hover[pressed=true]": f"background-color: {SLIGHTLY_DARKER_GREEN};",
                    },
                    "#stop": {
                        "": "border-bottom-right-radius: 5px;",
                        ":hover": f"background-color: {LIGHT_RED};",
                        ":pressed": f"background-color: {RED};",
                    },
                },
            },
            "WidgetSelectorComboBox > QComboBox": "width: 130px;padding-left: 35px;",
            "TimeSignatureSelector > ": {
                "SpinBox": "min-width: 50px;max-width: 50px;",
                "QComboBox": "padding-left: 12px;margin-left: -3px;min-width: 50px;max-width: 50px;",
            },
            "TuningDialog": {
                "": "min-height: 321px;max-height: 321px;min-width: 200px;max-width: 200px;",
                " > ": {
                    "QPushButton": "height: 23px;",
                    "TuningComboBox": "padding-left: 12px;min-width: 160px;max-width: 160px;",
                    "StringSelector ": {
                        "QLabel": "margin-left: 20px;",
                        "QComboBox": "margin-right: 20px;padding-left: 12px;min-width: 55px;max-width: 55px;",
                        "#string_selector_row": "min-height: 24px;max-height: 24px;",
                    },
                    "StringNumberSpinBox": "width: 35px;",
                },
            },
            "TuningSaveDialog": {
                "": "min-height: 123px;max-height: 123px;min-width: 200px;max-width: 200px;",
                " > QPushButton": "height: 23px;",
                " > QLineEdit": "height: 24px;",
            },
            "MidiDialog": {
                "": "min-height: 265px;max-height: 265px;min-width: 240px;max-width: 240px;",
                " > ": {
                    "MidiInputComboBox": "padding-left: 16px;",
                    "QPushButton": "height: 23px;",
                    "#refresh": "height: 16px;max-width: 130px;",
                },
            },
            "MidiAddDialog": {
                "": "min-height: 123px;max-height: 123px;min-width: 200px;max-width: 200px;",
                " > ": {
                    "QPushButton": "height: 23px;",
                    "QLineEdit": "height: 24px;",
                },
            },
            "PlayerDialog": {
                "": "min-height: 315px;max-height: 315px;min-width: 670px;max-width: 670px;",
                " ": {
                    "#system_players": {
                        " QLabel": "min-width: 105px;max-width: 105px;",
                        " #label_box > #settings_label": "margin-left: 110px;",
                    },
                    "#regular_players > #label_box > #settings_label": "margin-left: 5px;",
                    "#button_box": "min-width: 220px;max-width: 220px;",
                    "Button": "height: 23px;",
                    "PlayerRow": {
                        "": "min-height: 30px;max-height: 30px;",
                        " > ": {
                            "#instrument_name": "width: 110px;padding-left: 12px;margin-left: -8px;",
                            "#instrument_style": "width: 120px;padding-left: 12px;margin-left: -4px;",
                            "MidiOutputComboBox": "width: 145px;padding-left: 12px;margin-left: 11px;",
                            "MidiChannelComboBox": "width: 30px;padding-left: 12px;margin-left: -4px;",
                            "Button": {
                                "": "border-radius: 5px",
                                "#active": {
                                    "": (
                                        "margin-right: 3px;"
                                        "min-height: 23px;"
                                        "width: 72px;"
                                        f"background-color: {LIGHT_ORANGE};"
                                    ),
                                    ":hover": f"background-color: {SLIGHTLY_DARKER_ORANGE};",
                                    ":pressed": f"background-color: {DARKER_ORANGE};",
                                    ":hover[pressed=true]": f"background-color: {SLIGHTLY_DARKER_GREEN};",
                                    "[pressed=true]": f"background-color: {GREEN};",
                                    ":pressed[pressed=true]": f"background-color: {DARKER_GREEN};",
                                },
                                "#delete": {
                                    "": f"min-height: 23px;width: 55px;background-color: {LIGHT_RED};",
                                    ":hover": f"background-color: {RED};",
                                    ":pressed": f"background-color: {SLIGHTLY_DARKER_RED};",
                                },
                            },
                        },
                    },
                    "#label_box > #midi_settings_label": "margin-left: 158px;",
                },
            },
            "GuitarDisplayDialog": {
                " > QLabel": "margin-left: 5px;min-width: 60px;",
                " > QComboBox": "margin-left: -11px;padding-left: 21px;width: 130px;",
                " > PushPullButton": "margin-left: 30px;width: 130px;height: 18px;border-radius: 3px;",
                " GuitarDisplay": f"border: 1px solid {BORDER_COLOR};",
            },
            "PianoDisplayDialog": {" PianoDisplay": f"border: 1px solid {BORDER_COLOR};"},
            "DisplayContainerWidget": {
                "": "min-height: 71px;max-height: 71px;min-width: 80px;max-width: 80px;",
                " > PushPullButton": "height: 33.6%;",
                " > #guitar_button": "border-top-left-radius: 5px;border-top-right-radius: 5px;",
                " > #players_button": "border-bottom-left-radius: 5px;border-bottom-right-radius: 5px;",
            },
        }
    )
