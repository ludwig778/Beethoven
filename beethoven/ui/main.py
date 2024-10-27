import logging
import traceback

from PySide6.QtWidgets import QApplication

from beethoven.ui.setup import setup_main_window
from beethoven.ui.stylesheet import get_stylesheet
from beethoven.ui.utils import get_default_harmony_item

logger = logging.getLogger("ui.main")


def run():
    try:
        app = QApplication([])
        app.setStyleSheet(get_stylesheet())

        if 0:
            from beethoven.adapters.factory import get_adapters
            from beethoven.sequencer.runner import (Sequencer,
                                                    SequencerItemIterator,
                                                    SequencerParams)
            from beethoven.settings import setup_settings
            from beethoven.ui.dialogs.player import PlayerDialog
            from beethoven.ui.managers import AppManager

            adapters = get_adapters()
            manager = AppManager(settings=setup_settings(), adapters=adapters)

            from typing import List

            from beethoven.models import (Bpm, ChordItem, Degree, Duration,
                                          DurationItem, HarmonyItem, Scale,
                                          TimeSignature)

            def gen_harmony_items() -> List[HarmonyItem]:
                base_duration = Duration.parse("Q")

                harmony_items = []
                for scale, bpm, time_signature, chords in [
                    (
                        "C4_major",
                        "90",
                        "4/4",
                        [
                            ("I", Duration.parse("6Q")),
                            ("II", None),
                        ],
                    ),
                    (
                        "A4_minor",
                        "90",
                        "7/8",
                        [
                            ("IV", Duration.parse("3Q")),
                            ("V", Duration.parse("2Q")),
                            ("VI", None),
                        ],
                    ),
                    (
                        "E4_major",
                        "80",
                        "7/4",
                        [("IV", Duration.parse("4Q"))],
                    ),
                ]:
                    scale = Scale.parse(scale)
                    bpm = Bpm.parse(bpm)
                    time_signature = TimeSignature.parse(time_signature)

                    harmony_item = HarmonyItem(scale=scale, chord_items=[], bpm=bpm, time_signature=time_signature)
                    harmony_items.append(harmony_item)

                    for chord, duration in chords:
                        # chord = Chord.parse_with_scale_context(chord, scale=scale)

                        if duration:
                            numerator = duration.value // base_duration.value

                            duration_item = DurationItem(numerator=numerator, base_duration=base_duration)
                        else:
                            duration_item = DurationItem()

                        # chord_item = ChordItem(root=chord, name=chord.name, duration_item=duration_item)
                        chord_item = ChordItem(root=Degree.parse(chord), name="", duration_item=duration_item)
                        harmony_item.chord_items.append(chord_item)

                return harmony_items

            harmony_items = gen_harmony_items()

            def to_next(harmony_item, chord_item):
                chord_index = harmony_item.chord_items.index(chord_item)
                next_chord_index = chord_index + 1

                if next_chord_index >= len(harmony_item.chord_items):
                    harmony_index = harmony_items.index(harmony_item)
                    next_harmony_index = harmony_index + 1

                    harmony_item = harmony_items[next_harmony_index % len(harmony_items)]
                    chord_item = harmony_item.chord_items[0]
                else:
                    chord_item = harmony_item.chord_items[next_chord_index]

                return harmony_item, chord_item

            item_iterator = SequencerItemIterator.setup(
                current_items=(harmony_items[0], harmony_items[0].chord_items[0]),
                # next_items=(harmony_items[0], harmony_items[0].chord_items[1]),
                next_items_updater=to_next
            )
            params = SequencerParams(item_iterator=item_iterator)

            seq = Sequencer(midi_adapter=adapters.midi)
            seq.setup(params)

            seq.run()

            print()
            print()
        elif 0:
            from time import sleep

            from beethoven.adapters.factory import get_adapters
            from beethoven.sequencer.runner import (Sequencer,
                                                    SequencerItemIterator,
                                                    SequencerParams)
            from beethoven.settings import setup_settings
            from beethoven.ui.dialogs.player import PlayerDialog
            from beethoven.ui.managers import AppManager

            adapters = get_adapters()
            manager = AppManager(settings=setup_settings(), adapters=adapters)

            harmony_item = get_default_harmony_item()
            chord_item = harmony_item.chord_items[0]

            players = manager.sequencer.get_players()
            print(players)
            players = players[:1]
            print(players)

            harmony_item.bpm.value = 160

            params = SequencerParams(
                item_iterator=SequencerItemIterator.setup(
                    current_items=(harmony_item, chord_item),
                    next_items_updater=lambda *_: (harmony_item, chord_item),
                ),
                players=players,
            )
            seq = Sequencer(midi_adapter=adapters.midi)
            seq.params = params

            sleep(1.6)

            seq.run()
        elif 0:
            from beethoven.adapters.factory import get_adapters
            from beethoven.settings import setup_settings
            from beethoven.ui.dialogs.player import PlayerDialog
            from beethoven.ui.managers import AppManager

            manager = AppManager(settings=setup_settings(), adapters=get_adapters())

            players_dialog = PlayerDialog(manager=manager)
            players_dialog.show()
        else:
            main_window = setup_main_window()
            main_window.show()

            app.exec()

        # app.exec()
    except Exception:
        logger.critical(traceback.format_exc())


if __name__ == "__main__":
    run()
