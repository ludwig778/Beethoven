import logging
from itertools import cycle
from os import environ
from pprint import pprint
from typing import List

from pytest import fixture, raises

from beethoven.adapters.factory import get_adapters
from beethoven.helpers.sequencer import (BaseSorter, NoteSorter, note_repeater,
                                         note_sequencer, one_time_play)
from beethoven.models import (Bpm, Chord, ChordItem, Degree, Duration,
                              DurationItem, HarmonyItem, Interval, Note, Scale,
                              TimeSignature)
from beethoven.sequencer.instruments import BasicArpeggioPiano, BasicChordPiano, BasicDrum, BasicEighthMetronome, BasicMetronome
from beethoven.sequencer.objects import (BasePlayer, Mapping, Message,
                                         PercussionPlayer, SystemPlayer)
from beethoven.sequencer.objects import (Conductor, HarmonyItemSelector,
                                        InvalidHarmonyChordItems, Part,
                                        Splitter)
from beethoven.sequencer.utils import system_tick_logger
from beethoven.settings import AppSettings, MidiSettings, PlayerSetting
from beethoven.ui.constants import DEFAULT_BPM, DEFAULT_TIME_SIGNATURE
from beethoven.ui.managers.app import AppManager
from beethoven.ui.utils import get_default_harmony_items

logger = logging.getLogger("testing")


def get_default_harmony_items() -> List[HarmonyItem]:
    return [
        HarmonyItem(
            scale=Scale.parse("C4_major"),
            bpm=DEFAULT_BPM,
            time_signature=DEFAULT_TIME_SIGNATURE,
            chord_items=[
                ChordItem(
                    root=Degree.parse("II"),
                    name="",
                    duration_item=DurationItem(base_duration=Duration.parse("4")),
                ),
                ChordItem(
                    root=Degree.parse("V"),
                    name="",
                    duration_item=DurationItem(base_duration=Duration.parse("2")),
                ),
                ChordItem(
                    root=Degree.parse("I"),
                    name="",
                    duration_item=DurationItem(base_duration=Duration.parse("2")),
                ),
            ],
        ),
    ]

    
def create_message(note, duration, player=PlayerSetting(enabled=True), velocity=127, **kwargs):
    return Message(player=player, note=note, duration=duration, velocity=velocity, **kwargs)


def get_parts(harmony_items=get_default_harmony_items(), conductor_str=""):
    splitter = Splitter(conductor=Conductor.build(conductor_str))
    
    harmony_iterator = HarmonyItemSelector(harmony_items)
    parts = list(
        splitter.run(
            harmony_iterator.current_items,
            harmony_iterator.get_next_items()
        ) 
    )
    assert len(parts) == 1
    return parts

print()
print()
print()
"""
Part(start_cursor=0.0,
     intermediate_cursor=4.0,
     end_cursor=4.0,
     end_bar_cursor=4.0,
     end_harmony_cursor=4.0,
     global_cursor=0.0,
     split_duration=4.0,
     chord_duration=4.0,
     section=Section(symbol='M', current=1, count=1),
     bar_starting=True,
     chord_starting=True,
     harmony_starting=True,
     start_time_section=TimeSection(bar=1, measure=1, rest=Fraction(0, 1)))
"""

def test_one_time_play():
    start_cursor = Duration.parse("1")
    message1, message2 = object(), object()

    player = one_time_play(start_cursor, [message1, message2])

    assert next(player) == (Duration(1.0), message1)
    assert next(player) == (Duration(1.0), message2)

    with raises(StopIteration):
        next(player)


def test_note_repeater():
    whole = Duration.parse("4")
    message = object()

    player = note_repeater(whole, [message])

    assert next(player) == (Duration(0.0), message)
    assert next(player) == (Duration(4.0), message)

def test_note_repeater_with_offset():
    whole = Duration.parse("4")
    eighth = Duration.parse("1/2")
    message = object()

    player = note_repeater(whole, [message], eighth)

    assert next(player) == (Duration(0.5), message)
    assert next(player) == (Duration(4.5), message)

def test_note_sequencer():
    quarter = Duration.parse("1")
    message = object()

    player = note_sequencer(quarter, [message], "++.+")

    assert next(player) == (Duration(0.0), message)
    assert next(player) == (Duration(1.0), message)
    assert next(player) == (Duration(3.0), message)
    assert next(player) == (Duration(4.0), message)

def test_note_sorter():
    half = Duration.parse("2")
    quarter = Duration.parse("1")
    eighth = Duration.parse("1/2")

    kick_message = object()
    snare_message = object()
    hh_message = object()

    player = NoteSorter(
        kick=note_sequencer(half, [kick_message], "+."),
        snare=note_sequencer(quarter, [snare_message], "..+."),
        hh=note_sequencer(eighth, [hh_message], "+.+."),
    )

    assert next(player) == (Duration(0.0), kick_message)
    assert next(player) == (Duration(0.0), hh_message)

    assert next(player) == (Duration(1.0), hh_message)

    assert next(player) == (Duration(2.0), snare_message)
    assert next(player) == (Duration(2.0), hh_message)

    assert next(player) == (Duration(3.0), hh_message)

    assert next(player) == (Duration(4.0), kick_message)
    assert next(player) == (Duration(4.0), hh_message)


def test_basic_metronome_player():
    part = get_parts()[0]

    player = BasicMetronome(PlayerSetting())
    player.setup(part)

    main_tick = player.get_note(player.MAIN_TICK)
    sec_tick = player.get_note(player.SEC_TICK)

    assert next(player) == (Duration(0.0), main_tick)
    assert next(player) == (Duration(1.0), sec_tick)
    assert next(player) == (Duration(2.0), sec_tick)
    assert next(player) == (Duration(3.0), sec_tick)
    assert next(player) == (Duration(4.0), main_tick)


def test_basic_eighth_metronome_player():
    part = get_parts()[0]

    player = BasicEighthMetronome(PlayerSetting())
    player.setup(part)

    main_tick = player.get_note(player.MAIN_TICK)
    sec_tick = player.get_note(player.SEC_TICK)
    alt_tick = player.get_note(player.ALT_TICK)

    assert next(player) == (Duration(0.0), main_tick)
    assert next(player) == (Duration(0.5), alt_tick)
    assert next(player) == (Duration(1.0), sec_tick)
    assert next(player) == (Duration(1.5), alt_tick)
    assert next(player) == (Duration(2.0), sec_tick)
    assert next(player) == (Duration(2.5), alt_tick)
    assert next(player) == (Duration(3.0), sec_tick)
    assert next(player) == (Duration(3.5), alt_tick)
    assert next(player) == (Duration(4.0), main_tick)
    assert next(player) == (Duration(4.5), alt_tick)


def test_basic_chord_piano_player():
    whole = Duration.parse("4")

    part = get_parts()[0]
    player = BasicChordPiano(PlayerSetting())
    player.setup(part)

    def get_message(note):
        return create_message(note, duration=whole, player=player)

    assert next(player) == (Duration(0.0), get_message(Note.parse("D4")))
    assert next(player) == (Duration(0.0), get_message(Note.parse("F4")))
    assert next(player) == (Duration(0.0), get_message(Note.parse("A4")))
    assert next(player) == (Duration(0.0), get_message(Note.parse("C5")))

    with raises(StopIteration):
        next(player)


def test_basic_arpeggio_piano_player():
    whole = Duration.parse("4")

    part = get_parts()[0]
    player = BasicArpeggioPiano(PlayerSetting())
    player.setup(part)

    def get_message(note):
        return create_message(note, duration=whole, player=player)

    assert next(player) == (Duration(0.0), get_message(Note.parse("D4")))
    assert next(player) == (Duration(1.0), get_message(Note.parse("F4")))
    assert next(player) == (Duration(2.0), get_message(Note.parse("A4")))
    assert next(player) == (Duration(3.0), get_message(Note.parse("C5")))
    assert next(player) == (Duration(4.0), get_message(Note.parse("D5")))
    assert next(player) == (Duration(5.0), get_message(Note.parse("F5")))
    assert next(player) == (Duration(6.0), get_message(Note.parse("A5")))
    assert next(player) == (Duration(7.0), get_message(Note.parse("C6")))
    assert next(player) == (Duration(8.0), get_message(Note.parse("D6")))
    assert next(player) == (Duration(9.0), get_message(Note.parse("C6")))
    assert next(player) == (Duration(10.0), get_message(Note.parse("A5")))


def test_basic_drum_player():
    part = get_parts()[0]

    player = BasicDrum(PlayerSetting())
    player.setup(part)

    kick = player.get_note(player.KICK)
    snare = player.get_note(player.SNARE)
    hh = player.get_note(player.CLOSED_HH)
    crash = player.get_note(player.CRASH)

    assert next(player) == (Duration(0.0), kick)
    assert next(player) == (Duration(0.0), hh)
    assert next(player) == (Duration(0.0), crash)
    assert next(player) == (Duration(1.0), hh)
    assert next(player) == (Duration(2.0), snare)
    assert next(player) == (Duration(2.0), hh)
    assert next(player) == (Duration(3.0), hh)
    assert next(player) == (Duration(4.0), kick)
    assert next(player) == (Duration(4.0), hh)


def test_system_player():
    part = get_parts()[0]
    player_obj = SystemPlayer(PlayerSetting())
    player = player_obj.play(part)

    for i in range(4):
        cursor, func = next(player)
        
        assert cursor == Duration(i)
        assert callable(func)

