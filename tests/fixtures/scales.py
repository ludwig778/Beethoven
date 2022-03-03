from beethoven.models import Interval, Note, Scale
from tests.fixtures.chords import a_min7, b_min7b5, c_maj7, d_min7, e_min7, f_maj7, g_7

c_major = Scale(
    tonic=Note(name="C"),
    name="major",
    notes=[
        Note(name="C"),
        Note(name="D"),
        Note(name="E"),
        Note(name="F"),
        Note(name="G"),
        Note(name="A"),
        Note(name="B"),
    ],
    intervals=[
        Interval(name="1"),
        Interval(name="2"),
        Interval(name="3"),
        Interval(name="4"),
        Interval(name="5"),
        Interval(name="6"),
        Interval(name="7"),
    ],
)
c_major_7th_chords = [c_maj7, d_min7, e_min7, f_maj7, g_7, a_min7, b_min7b5]

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
