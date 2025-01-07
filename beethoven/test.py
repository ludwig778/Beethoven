from beethoven.adapters.midi import MidiAdapter


m = MidiAdapter()

print()
print("=== MIDI CHECK ===")
print()
print(m.available_inputs)
midi_input = m.open_input("MPK mini 3")
print(midi_input)
from mido.backends.rtmidi import Input, Output
print("Listening:")
print()

try:
    for i in range(40):
        msg = midi_input.receive()

        if msg.value == 127:
            print(f"{i:2} : {msg}")
except KeyboardInterrupt:
    pass

midi_input.close()
print()
print("Closed:", midi_input.closed)