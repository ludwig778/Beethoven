from pytest import mark

from beethoven.sequencer.note_duration import Eighths, Quarter
from beethoven.sequencer.play_room import PlayRoom
from beethoven.sequencer.players.base import Players
from beethoven.sequencer.tempo import default_tempo_factory
from beethoven.sequencer.time_signature import default_time_signature_factory


def test_play_room():
    play_room = PlayRoom()
    #play_room.players.add(Players.get("Metronome"))
    play_room.players.add(Players.get("Drum"))
    #play_room.players.add(Players.get("Piano"))

    #play_room._parse_grid("A2 major maj I,V,ii,Vmin_maj7,Vbbmin_maj7,IVsus2")
    play_room._parse_grid("G2 major maj VI7", repeat=True)