from functools import partial

from beethoven.repository.midi import midi
from beethoven.sequencer.note import Note


def test_midi_play(monkeypatch):
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

    def get_messages(msg, messages=None):
        messages.append({
            "type": msg.type,
            "channel": msg.channel,
            "note": msg.note,
            "velocity": msg.velocity,
            "time": msg.time
        })

    messages = []
    monkeypatch.setattr(midi, "_send_msg", partial(get_messages, messages=messages))

    midi.play(timeline, length)

    assert messages == [
        {'type': 'note_on',  'channel': 0, 'note': 69, 'velocity': 127, 'time': 0},
        {'type': 'note_on',  'channel': 0, 'note': 73, 'velocity': 127, 'time': 0},
        {'type': 'note_on',  'channel': 1, 'note': 62, 'velocity': 63,  'time': 0},
        {'type': 'note_off', 'channel': 1, 'note': 62, 'velocity': 127, 'time': 0.020833333333333332},
        {'type': 'note_on',  'channel': 1, 'note': 62, 'velocity': 63,  'time': 0},
        {'type': 'note_off', 'channel': 0, 'note': 69, 'velocity': 127, 'time': 0.020833333333333332},
        {'type': 'note_off', 'channel': 0, 'note': 73, 'velocity': 127, 'time': 0},
        {'type': 'note_off', 'channel': 1, 'note': 62, 'velocity': 127, 'time': 0}
    ]
