from beethoven.players.drum import Drum
from beethoven.players.piano import Piano
from beethoven.sequencer.jam_room import JamRoom


class State:
    def __init__(self):
        self.jam_room = JamRoom()

        self.jam_room.players.add(Piano())
        self.jam_room.players.add(Drum())


state = State()
