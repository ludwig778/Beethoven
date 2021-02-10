from pytest import mark

from beethoven.sequencer.note_duration import Eighths, Quarter
from beethoven.sequencer.players.base import Players
from beethoven.sequencer.tempo import default_tempo_factory
from beethoven.sequencer.time_signature import default_time_signature_factory


@mark.parametrize("note_duration,length", [
    (Quarter, 4),
    (Eighths, 8),
])
def test_instrument_metronome(note_duration, length):
    players = Players()
    player = players.get("Metronome")
    player.prepare(
        time_signature=default_time_signature_factory(),
        tempo=default_tempo_factory(),
        duration=note_duration
    )

    to_play = list(player.play_measure())

    assert len(to_play) == length
