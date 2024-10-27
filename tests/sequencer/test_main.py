import logging
from os import environ
from pprint import pprint

from pytest import fixture, raises

from beethoven.adapters.factory import get_adapters
from beethoven.models import (Bpm, Chord, ChordItem, Degree, Duration,
                              DurationItem, HarmonyItem, Scale, TimeSignature)
from beethoven.sequencer.objects import (HarmonyItemSelector,
                                        InvalidHarmonyChordItems)
from beethoven.sequencer.utils import system_tick_logger
from beethoven.settings import AppSettings
from beethoven.ui.managers.app import AppManager
from beethoven.ui.utils import get_default_harmony_items

a_major = Scale.parse("A_major")
d_minor = Scale.parse("D_minor")
g_mixolydian = Scale.parse("G_mixolydian")

chord_item_11 = ChordItem(root=Degree("II"), name="", duration_item=Duration())
chord_item_12 = ChordItem(root=Degree("V"), name="", duration_item=Duration())
chord_item_13 = ChordItem(root=Degree("I"), name="", duration_item=Duration())
chord_item_21 = ChordItem(root=Degree("II"), name="", duration_item=Duration())
chord_item_22 = ChordItem(root=Degree("V"), name="", duration_item=Duration())
chord_item_23 = ChordItem(root=Degree("I"), name="", duration_item=Duration())
chord_item_24 = ChordItem(root=Degree("IV"), name="", duration_item=Duration())
chord_item_31 = ChordItem(root=Degree("VI"), name="", duration_item=Duration())
chord_item_32 = ChordItem(root=Degree("III"), name="", duration_item=Duration())

@fixture
def harmony_item_1():
    return HarmonyItem(
        scale=a_major,
        chord_items=[chord_item_11, chord_item_12, chord_item_13],
        bpm=Bpm(120),
        time_signature=TimeSignature(4, 4)
    )

@fixture
def harmony_item_2():
    return HarmonyItem(
        scale=d_minor,
        chord_items=[chord_item_21, chord_item_22, chord_item_23],
        bpm=Bpm(90),
        time_signature=TimeSignature(6, 4)
    )

@fixture
def harmony_item_3():
    return HarmonyItem(
        scale=g_mixolydian,
        chord_items=[chord_item_31],
        bpm=Bpm(75),
        time_signature=TimeSignature(3, 2)
    )

@fixture
def harmony_selector1(harmony_item_1, harmony_item_2):
    return HarmonyItemSelector([harmony_item_1, harmony_item_2])

logger = logging.getLogger("testing")

def test_harmony_item_selector(harmony_selector1, monkeypatch):
    #monkeypatch.delenv("BEETHOVEN_CONFIG_PATH")
    
    manager = AppManager(settings=AppSettings.load(), adapters=get_adapters())
    harmony_items = get_default_harmony_items()
    harmony_iterator = HarmonyItemSelector(harmony_items)
    #def on_chord_item_change(*args, **kwargs):
    #    print(args)
    #    print(kwargs)
    """
    params = SequencerParams(
        item_iterator=harmony_iterator,
        players=manager.sequencer_manager.get_players(),
        on_chord_item_change=on_chord_item_change, #manager.sequencer_manager.items_change.emit,
        on_tick=system_tick_logger(logger, level=logging.DEBUG),
    )
    """

    #print("=" * 123)

    """
    print(manager.sequencer_manager.sequencer)
    players = manager.sequencer_manager.get_players()
    preview = manager.sequencer_manager.get_players(True)
    print()

    s = manager.sequencer_manager.sequencer

    s.run(harmony_iterator, preview)



    print()

    """
