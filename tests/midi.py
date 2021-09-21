from fractions import Fraction
from timeit import timeit

from mido import Message, MetaMessage, MidiFile, MidiTrack
from pytest import mark

from beethoven.midi import get_midi_file, play_midi_file
from beethoven.objects import Grid
from beethoven.player.base import Player


class FakePlayer(Player):
    def get_notes(self, section, duration):
        notes = [43]

        yield notes, section, duration


@mark.skip
@mark.parametrize(
    "players,grid,expected_midi_file,expected_elapsed",
    [
        (
            {0: FakePlayer()},
            "bpm=960 sc=A_major ts=4/4 p=I",
            MidiFile(
                type=1,
                ticks_per_beat=480,
                tracks=[
                    MidiTrack(
                        [
                            MetaMessage("text", text="0", time=Fraction(0, 1)),
                            Message("note_on", channel=0, note=43, velocity=64, time=0),
                            Message(
                                "note_off",
                                channel=0,
                                note=43,
                                velocity=64,
                                time=Fraction(11983, 200),
                            ),
                            Message("note_on", channel=0, note=43, velocity=64, time=0),
                            Message(
                                "note_off",
                                channel=0,
                                note=43,
                                velocity=64,
                                time=Fraction(11983, 200),
                            ),
                            Message("note_on", channel=0, note=43, velocity=64, time=0),
                            Message(
                                "note_off",
                                channel=0,
                                note=43,
                                velocity=64,
                                time=Fraction(11983, 200),
                            ),
                            Message("note_on", channel=0, note=43, velocity=64, time=0),
                            Message(
                                "note_off",
                                channel=0,
                                note=43,
                                velocity=64,
                                time=Fraction(11983, 200),
                            ),
                            MetaMessage("end_of_track", time=0),
                        ]
                    )
                ],
            ),
            0.25,
        ),
        (
            {0: FakePlayer()},
            "bpm=240 sc=A_major ts=1/4 p=I",
            MidiFile(
                type=1,
                ticks_per_beat=480,
                tracks=[
                    MidiTrack(
                        [
                            MetaMessage("text", text="0", time=Fraction(0, 1)),
                            Message("note_on", channel=0, note=43, velocity=64, time=0),
                            Message(
                                "note_off",
                                channel=0,
                                note=43,
                                velocity=64,
                                time=Fraction(11983, 50),
                            ),
                            MetaMessage("end_of_track", time=0),
                        ]
                    )
                ],
            ),
            0.25,
        ),
    ],
)
def test_grid_to_midi(players, grid, expected_midi_file, expected_elapsed):
    grid = Grid.parse(grid)

    midi_file = get_midi_file(grid, players)
    elapsed = timeit(lambda: list(play_midi_file(midi_file)), number=1)

    assert midi_file.__dict__ == expected_midi_file.__dict__
    assert expected_elapsed * 0.99 < elapsed < expected_elapsed * 1.01
