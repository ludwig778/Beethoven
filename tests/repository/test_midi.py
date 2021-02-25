from beethoven.repository.midi import midi
from beethoven.sequencer.note import Note


def test_midi_play():
    timeline = {
        0.0: [
            {
                'channel': 0,
                'duration': 0.04,
                'notes': (Note("A3"), Note("C#4")),
                'velocity': 127
            },
            {
                'channel': 1,
                'duration': 0.02,
                'notes': (Note("D3"),),
                'velocity': 63
            }
        ],
        0.02: [
            {
                'channel': 1,
                'duration': 0.02,
                'notes': (Note("D3"),),
                'velocity': 63
            }
        ]
    }
    length = 0.04

    midi.play(timeline, length)
    midi.play(timeline, length, repeat=2)

    assert midi
