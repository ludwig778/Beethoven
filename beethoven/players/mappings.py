from beethoven.sequencer.note import Note

metronome_mapping = {
    "TICK":     Note("A4"),
    "ALT_TICK": Note("B4"),
    "OFF_TICK": Note("C5")
}

drum_mapping = {
    "KICK":            Note("C1"),
    "SNARE":           Note("D1"),
    "CLOSE_HH":        Note("F#1"),
    "OPEN_HH":         Note("A#1"),
    "HIGH_TOM":        None,
    "MIDDLE_HIGH_TOM": None,
    "MIDDLE_TOM":      None,
    "MIDDLE_LOW_TOM":  None,
    "LOW_TOM":         None,
    "CLAP":            None,
    "RIDE":            None,
    "CYMBAL1":         Note("C2"),
    "CYMBAL2":         None,
    "CHINA":           None
}
