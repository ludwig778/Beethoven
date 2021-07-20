from pytest import mark

from beethoven.prompt.parser import prompt_harmony_list_parser
from beethoven.sequencer.grid import Grid, GridPart
from beethoven.sequencer.note_duration import Half
from beethoven.sequencer.tempo import Tempo
from beethoven.sequencer.time_signature import TimeSignature
from beethoven.theory.chord import Chord
from beethoven.theory.scale import Scale


@mark.parametrize("input_string,expected", [
    (
        "", Grid()
    ),
    (
        "n=A sc=major p=", Grid()
    ),
    (
        "n=A p=I", Grid()
    ),
    (
        "n=A sc=major p=I,i",
        Grid([
            GridPart(
                scale=Scale("A", "ionian"),
                chord=Chord("A", "maj7"),
                time_signature=TimeSignature(4, 4),
                tempo=Tempo(120),
            ),
            GridPart(
                scale=Scale("A", "ionian"),
                chord=Chord("A", "min7"),
                time_signature=TimeSignature(4, 4),
                tempo=Tempo(120),
            )
        ])
    ),
    (
        "n=A sc=major p=Amin7,Cmin7",
        Grid([
            GridPart(
                scale=Scale("A", "ionian"),
                chord=Chord("A", "min7"),
                time_signature=TimeSignature(4, 4),
                tempo=Tempo(120),
            ),
            GridPart(
                scale=Scale("A", "ionian"),
                chord=Chord("C", "min7"),
                time_signature=TimeSignature(4, 4),
                tempo=Tempo(120),
            ),
        ])
    ),
    (
        "n=A sc=major p=I;n=B sc=minor p=I",
        Grid([
            GridPart(
                chord=Chord("A", "maj7"),
                scale=Scale("A", "ionian"),
                time_signature=TimeSignature(4, 4),
                tempo=Tempo(120),
            ),
            GridPart(
                chord=Chord("B", "maj7"),
                scale=Scale("B", "aeolian"),
                time_signature=TimeSignature(4, 4),
                tempo=Tempo(120),
            ),
        ])
    ),
    (
        "n=A sc=major t=60 p=I;t=90 p=I",
        Grid([
            GridPart(
                scale=Scale("A", "ionian"),
                chord=Chord("A", "maj7"),
                time_signature=TimeSignature(4, 4),
                tempo=Tempo(60),
            ),
            GridPart(
                scale=Scale("A", "ionian"),
                chord=Chord("A", "maj7"),
                time_signature=TimeSignature(4, 4),
                tempo=Tempo(90)
            )
        ])
    ),
    (
        "n=A sc=major ts=3/2 p=I;ts=7/8 p=I",
        Grid([
            GridPart(
                scale=Scale("A", "ionian"),
                chord=Chord("A", "maj7"),
                time_signature=TimeSignature(3, 2),
                tempo=Tempo(120),
            ),
            GridPart(
                scale=Scale("A", "ionian"),
                chord=Chord("A", "maj7"),
                time_signature=TimeSignature(7, 8),
                tempo=Tempo(120),
            ),
        ])
    ),
    (
        "n=A sc=major p=I:d=H,I:d=2Q,I",
        Grid([
            GridPart(
                chord=Chord("A", "maj7"),
                scale=Scale("A", "ionian"),
                duration=Half,
                time_signature=TimeSignature(4, 4),
                tempo=Tempo(120),
            ),
            GridPart(
                scale=Scale("A", "ionian"),
                chord=Chord("A", "maj7"),
                duration=Half,
                time_signature=TimeSignature(4, 4),
                tempo=Tempo(120),
            ),
            GridPart(
                scale=Scale("A", "ionian"),
                chord=Chord("A", "maj7"),
                time_signature=TimeSignature(4, 4),
                tempo=Tempo(120),
            ),
        ])
    ),
    (
        "n=C sc=major p=Amaj7:i=1,Bmin7:i=2",
        Grid([
            GridPart(
                chord=Chord("A", "maj7", inversion=1),
                scale=Scale("C", "ionian"),
                time_signature=TimeSignature(4, 4),
                tempo=Tempo(120),
            ),
            GridPart(
                scale=Scale("C", "ionian"),
                chord=Chord("B", "min7", inversion=2),
                time_signature=TimeSignature(4, 4),
                tempo=Tempo(120),
            ),
        ])
    ),
    (
        "n=C sc=major p=V:b=ii",
        Grid([
            GridPart(
                scale=Scale("C", "ionian"),
                chord=Chord("A", "7"),
                time_signature=TimeSignature(4, 4),
                tempo=Tempo(120),
            ),
        ])
    ),
    (
        "n=C sc=major p=I:b=A,B:b=C",
        Grid([
            GridPart(
                scale=Scale("C", "ionian"),
                chord=Chord("C", "maj7", base_note="A"),
                time_signature=TimeSignature(4, 4),
                tempo=Tempo(120),
            ),
            GridPart(
                scale=Scale("C", "ionian"),
                chord=Chord("B", "maj", base_note="C"),
                time_signature=TimeSignature(4, 4),
                tempo=Tempo(120),
            ),
        ])
    ),
    (
        "n=C sc=major p=Gmin7:b=A,Dmaj:b=C",
        Grid([
            GridPart(
                chord=Chord("G", "min7", base_note="A"),
                scale=Scale("C", "ionian"),
                time_signature=TimeSignature(4, 4),
                tempo=Tempo(120),
            ),
            GridPart(
                chord=Chord("D", "maj", base_note="C"),
                scale=Scale("C", "ionian"),
                time_signature=TimeSignature(4, 4),
                tempo=Tempo(120),
            ),
        ])
    )
])
def test_prompt_harmony_list_parser(input_string, expected):
    assert prompt_harmony_list_parser(input_string, config={
        "time_signature": TimeSignature(4, 4),
        "tempo": Tempo(120),
    }) == expected
