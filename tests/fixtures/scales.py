from beethoven.models import Interval, Note, Scale


a_minor = Scale(
    tonic=Note(name="A"),
    name="minor",
    notes=[
        Note(name="A"),
        Note(name="B"),
        Note(name="C"),
        Note(name="D"),
        Note(name="E"),
        Note(name="F"),
        Note(name="G"),
    ],
    intervals=[
        Interval(name="1"),
        Interval(name="2"),
        Interval(name="3", alteration=-1),
        Interval(name="4"),
        Interval(name="5"),
        Interval(name="6", alteration=-1),
        Interval(name="7", alteration=-1),
    ],
)

a_minor_pentatonic = Scale(
    tonic=Note(name="A"),
    name="pentatonic",
    notes=[
        Note(name="A"),
        Note(name="C"),
        Note(name="D"),
        Note(name="E"),
        Note(name="G"),
    ],
    intervals=[
        Interval(name="1"),
        Interval(name="3", alteration=-1),
        Interval(name="4"),
        Interval(name="5"),
        Interval(name="7", alteration=-1),
    ],
)
