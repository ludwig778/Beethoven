from beethoven.objects import (Bpm, Chord, Degree, Duration, Grid, Interval,
                               Note, Scale, TimeSignature)
from beethoven.toolbox import (add_interval_to_note, get_base_time,
                               get_chords_from_scale, get_list_parser,
                               get_note_index, get_notes_intervals, get_parser,
                               get_timespan, multiply_duration,
                               substract_interval_to_note,
                               time_signature_as_duration)

enrichment_matrix = {
    Bpm: {
        "parse": staticmethod(get_parser("bpm")),
        "base_time": property(get_base_time)
    },
    Degree: {
        "parse": staticmethod(get_parser("degree"))
    },
    Chord: {
        "parse": staticmethod(get_parser("chord"))
    },
    Scale: {
        "parse": staticmethod(get_parser("scale")),
        "get_chords": get_chords_from_scale
    },
    Note: {
        "parse": staticmethod(get_parser("note")),
        "parse_list": staticmethod(get_list_parser("note")),
        "index": property(get_note_index),
        "__add__": add_interval_to_note,
        "__sub__": substract_interval_to_note,
        "__truediv__": get_notes_intervals
    },
    Interval: {
        "parse": staticmethod(get_parser("interval")),
        "parse_list": staticmethod(get_list_parser("interval"))
    },
    TimeSignature: {
        "parse": staticmethod(get_parser("time_signature")),
        "as_duration": property(time_signature_as_duration)
    },
    Duration: {
        "parse": staticmethod(get_parser("duration")),
        "get_timespan": get_timespan,
        "__mul__": multiply_duration
    },
    Grid: {
        "parse": staticmethod(get_parser("grid"))
    },
}


for cls, methods in enrichment_matrix.items():
    for method_name, func in methods.items():
        setattr(cls, method_name, func)
