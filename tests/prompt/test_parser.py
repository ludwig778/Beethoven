from pytest import mark

from beethoven.prompt.parser import prompt_harmony_list_parser
from beethoven.sequencer.note_duration import Half
from beethoven.sequencer.tempo import Tempo
from beethoven.sequencer.time_signature import TimeSignature
from beethoven.theory.chord import Chord
from beethoven.theory.scale import Scale


@mark.parametrize("input_string,expected", [
    (
        "", []
    ),
    (
        "n=A sc=major p=", []
    ),
    (
        "n=A p=I", []
    ),
    (
        "n=A sc=major p=I,i", [
            {
                "chord": Chord("A", "maj7"),
                "scale": Scale("A", "ionian"),
            },
            {
                "chord": Chord("A", "min7")
            }
        ]
    ),
    (
        "n=A sc=major p=Amin7,Cmin7", [
            {
                "chord": Chord("A", "min7"),
                "scale": Scale("A", "ionian"),
            },
            {
                "chord": Chord("C", "min7")
            }
        ]
    ),
    (
        "n=A sc=major p=I;n=B sc=minor p=I", [
            {
                "chord": Chord("A", "maj7"),
                "scale": Scale("A", "ionian"),
            },
            {
                "chord": Chord("B", "maj7"),
                "scale": Scale("B", "aeolian")
            }
        ]
    ),
    (
        "n=A sc=major t=60 p=I;t=90 p=I", [
            {
                "chord": Chord("A", "maj7"),
                "scale": Scale("A", "ionian"),
                "tempo": Tempo(60),
            },
            {
                "chord": Chord("A", "maj7"),
                "tempo": Tempo(90)
            }
        ]
    ),
    (
        "n=A sc=major ts=3/2 p=I;ts=7/8 p=I", [
            {
                "chord": Chord("A", "maj7"),
                "scale": Scale("A", "ionian"),
                "time_signature": TimeSignature(3, 2),
            },
            {
                "chord": Chord("A", "maj7"),
                "time_signature": TimeSignature(7, 8)
            }
        ]
    ),
    (
        "n=A sc=major p=I:d=H,I:d=2Q,I", [
            {
                "chord": Chord("A", "maj7"),
                "scale": Scale("A", "ionian"),
                "duration": Half
            },
            {
                "chord": Chord("A", "maj7"),
                "duration": Half
            },
            {
                "chord": Chord("A", "maj7"),
            }
        ]
    ),
    (
        "n=C sc=major p=Amaj7:i=1,Bmin7:i=2", [
            {
                "chord": Chord("A", "maj7", inversion=1),
                "scale": Scale("C", "ionian"),
            },
            {
                "chord": Chord("B", "min7", inversion=2)
            }
        ]
    ),
    (
        "n=C sc=major p=V:b=ii,ii", [
            {
                "chord": Chord("A", "7"),
                "scale": Scale("C", "ionian"),
            },
            {
                "chord": Chord("D", "min7")
            }
        ]
    ),
    (
        "n=C sc=major p=I:b=A,B:b=C", [
            {
                "chord": Chord("C", "maj7", base_note="A"),
                "scale": Scale("C", "ionian"),
            },
            {
                "chord": Chord("B", "maj", base_note="C")
            }
        ]
    ),
    (
        "n=C sc=major p=Gmin7:b=A,Dmaj:b=C", [
            {
                "chord": Chord("G", "min7", base_note="A"),
                "scale": Scale("C", "ionian"),
            },
            {
                "chord": Chord("D", "maj", base_note="C")
            }
        ]
    )
])
def test_prompt_harmony_list_parser(input_string, expected):
    assert prompt_harmony_list_parser(input_string) == expected
