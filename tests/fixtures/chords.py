from beethoven.models import Chord, Interval, Note

c_maj7 = Chord(
    root=Note(name="C"),
    name="maj7",
    notes=[
        Note(name="C"),
        Note(name="E"),
        Note(name="G"),
        Note(name="B"),
    ],
    intervals=[
        Interval(name="1"),
        Interval(name="3"),
        Interval(name="5"),
        Interval(name="7"),
    ],
)

d_min7 = Chord(
    root=Note(name="D"),
    name="min7",
    notes=[
        Note(name="D"),
        Note(name="F"),
        Note(name="A"),
        Note(name="C"),
    ],
    intervals=[
        Interval(name="1"),
        Interval(name="3", alteration=-1),
        Interval(name="5"),
        Interval(name="7", alteration=-1),
    ],
)

e_min7 = Chord(
    root=Note(name="E"),
    name="min7",
    notes=[
        Note(name="E"),
        Note(name="G"),
        Note(name="B"),
        Note(name="D"),
    ],
    intervals=[
        Interval(name="1"),
        Interval(name="3", alteration=-1),
        Interval(name="5"),
        Interval(name="7", alteration=-1),
    ],
)

f_maj7 = Chord(
    root=Note(name="F"),
    name="maj7",
    notes=[
        Note(name="F"),
        Note(name="A"),
        Note(name="C"),
        Note(name="E"),
    ],
    intervals=[
        Interval(name="1"),
        Interval(name="3"),
        Interval(name="5"),
        Interval(name="7"),
    ],
)

g_7 = Chord(
    root=Note(name="G"),
    name="7",
    notes=[
        Note(name="G"),
        Note(name="B"),
        Note(name="D"),
        Note(name="F"),
    ],
    intervals=[
        Interval(name="1"),
        Interval(name="3"),
        Interval(name="5"),
        Interval(name="7", alteration=-1),
    ],
)

a_min7 = Chord(
    root=Note(name="A"),
    name="min7",
    notes=[
        Note(name="A"),
        Note(name="C"),
        Note(name="E"),
        Note(name="G"),
    ],
    intervals=[
        Interval(name="1"),
        Interval(name="3", alteration=-1),
        Interval(name="5"),
        Interval(name="7", alteration=-1),
    ],
)

b_min7b5 = Chord(
    root=Note(name="B"),
    name="min7b5",
    notes=[
        Note(name="B"),
        Note(name="D"),
        Note(name="F"),
        Note(name="A"),
    ],
    intervals=[
        Interval(name="1"),
        Interval(name="3", alteration=-1),
        Interval(name="5", alteration=-1),
        Interval(name="7", alteration=-1),
    ],
)
