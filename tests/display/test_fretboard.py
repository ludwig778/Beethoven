from pytest import mark

from beethoven.common.tuning import (B_STANDARD_7, E_STANDARD, E_STANDARD_BASS,
                                     Tuning)
from beethoven.display.fretboard import Fretboard
from beethoven.theory.chord import Chord
from beethoven.theory.note import Note
from beethoven.theory.scale import Scale


@mark.parametrize("tuning,fretboard_kwargs,call_kwargs,expected_ascii", [
    # Test without any scale/chord
    (
        Tuning(Note("A")),
        {},
        {},
        (
            "     ║     |     |     |     |     |     |     |     |     |     |     |     |\n"
            "\n"
            "  0  ║     |     |  3  |     |  5  |     |  7  |     |  9  |     |     | 12  |"
        )
    ),
    # Test with a scale
    (
        Tuning(Note("A")),
        {},
        {"scale": Scale("A", "major")},
        (
            "  A  ║     |  B  |     | C#  |  D  |     |  E  |     | F#  |     | G#  |  A  |\n"
            "\n"
            "  0  ║     |     |  3  |     |  5  |     |  7  |     |  9  |     |     | 12  |"
        )
    ),
    # Test with a chord
    (
        Tuning(Note("A")),
        {},
        {"chord": Chord("A", "maj7")},
        (
            "  A  ║     |     |     | C#  |     |     |  E  |     |     |     | G#  |  A  |\n"
            "\n"
            "  0  ║     |     |  3  |     |  5  |     |  7  |     |  9  |     |     | 12  |"
        )
    ),
    # Test shifting first and last frets on initialization
    (
        Tuning(Note("A")),
        {"first_fret": 3, "last_fret": 9},
        {"scale": Scale("A", "major")},
        (
            "     | C#  |  D  |     |  E  |     | F#  |\n"
            "\n"
            "  3  |     |  5  |     |  7  |     |  9  |"
        )
    ),
    # Test shifting first and last frets on method call
    (
        Tuning(Note("A")),
        {},
        {"scale": Scale("A", "major"), "first_fret": 3, "last_fret": 9},
        (
            "     | C#  |  D  |     |  E  |     | F#  |\n"
            "\n"
            "  3  |     |  5  |     |  7  |     |  9  |"
        )
    ),
    # Test with more strings
    (
        Tuning(*Note.to_list("E,A,D")),
        {},
        {"scale": Scale("A", "major")},
        (
            "  D  ║     |  E  |     | F#  |     | G#  |  A  |     |  B  |     | C#  |  D  |\n"
            "  A  ║     |  B  |     | C#  |  D  |     |  E  |     | F#  |     | G#  |  A  |\n"
            "  E  ║     | F#  |     | G#  |  A  |     |  B  |     | C#  |  D  |     |  E  |\n"
            "\n"
            "  0  ║     |     |  3  |     |  5  |     |  7  |     |  9  |     |     | 12  |"
        )
    ),
    # Test with more strings on less frets
    (
        Tuning(*Note.to_list("E,A,D")),
        {"last_fret": 4},
        {"scale": Scale("A", "major")},
        (
            "  D  ║     |  E  |     | F#  |\n"
            "  A  ║     |  B  |     | C#  |\n"
            "  E  ║     | F#  |     | G#  |\n"
            "\n"
            "  0  ║     |     |  3  |  4  |"
        )
    ),
    # Test with some coloring #1 (tonic_color)
    (
        Tuning(*Note.to_list("E,A,D")),
        {"last_fret": 4, "config": {"tonic_color": "white"}},
        {"scale": Scale("A", "major")},
        (
            "  D  ║     |  E  |     | F#  |\n"
            "\x1b[38;5;15m  A  \x1b[0m║     |  B  |     | C#  |\n"
            "  E  ║     | F#  |     | G#  |\n"
            "\n"
            "  0  ║     |     |  3  |  4  |"
        )
    ),
    # Test with some coloring #2 (chord_color)
    (
        Tuning(*Note.to_list("E,A,D")),
        {"last_fret": 4, "config": {"chord_color": "red"}},
        {"scale": Scale("A", "major"), "chord": Chord("A#", "min")},
        (
            "  D  ║     |  E  |\x1b[38;5;1m E#  \x1b[0m| F#  |\n"
            "  A  ║\x1b[38;5;1m A#  \x1b[0m|  B  |     |\x1b[38;5;1m C#  \x1b[0m|\n"
            "  E  ║\x1b[38;5;1m E#  \x1b[0m| F#  |     | G#  |\n"
            "\n"
            "  0  ║     |     |  3  |  4  |"
        )
    ),
    # Test with some coloring #3 (chord_attr)
    (
        Tuning(*Note.to_list("E,A,D")),
        {"last_fret": 4, "config": {"chord_attr": "bold"}},
        {"scale": Scale("A", "major"), "chord": Chord("A#", "min")},
        (
            "  D  ║     |  E  |\x1b[1m E#  \x1b[0m| F#  |\n"
            "  A  ║\x1b[1m A#  \x1b[0m|  B  |     |\x1b[1m C#  \x1b[0m|\n"
            "  E  ║\x1b[1m E#  \x1b[0m| F#  |     | G#  |\n"
            "\n"
            "  0  ║     |     |  3  |  4  |"
        )
    ),
    # Test with some coloring #4 (diatonic_color)
    (
        Tuning(*Note.to_list("E,A,D")),
        {"last_fret": 4, "config": {"diatonic_color": {0: "red", 2: "yellow", 4: "green"}}},
        {"scale": Scale("A", "major")},
        (
            "  D  ║     |\x1b[38;5;2m  E  \x1b[0m|     | F#  |\n"
            "  A  ║     |  B  |     |\x1b[38;5;3m C#  \x1b[0m|\n"
            "\x1b[38;5;2m  E  \x1b[0m║     | F#  |     | G#  |\n"
            "\n"
            "  0  ║     |     |  3  |  4  |"
        )
    ),
    # Test with some coloring #5 (scale_color) => non diatonic
    (
        Tuning(*Note.to_list("E,A,D")),
        {"last_fret": 4, "config": {"scale_color": {0: "blue", 2: "magenta", 4: "cyan"}}},
        {"scale": Scale("A", "whole tone")},
        (
            "     ║ D#  |     |\x1b[38;5;6m  F  \x1b[0m|     |\n"
            "  A  ║     |  B  |     |\x1b[38;5;5m C#  \x1b[0m|\n"
            "     ║\x1b[38;5;6m  F  \x1b[0m|     |  G  |     |\n"
            "\n"
            "  0  ║     |     |  3  |  4  |"
        )
    ),
    # Test with some coloring #6, mix all the above
    (
        Tuning(*Note.to_list("E,A,D")),
        {
            "last_fret": 4,
            "config": {
                "tonic_color": "white",
                "chord_color": "yellow",
                "chord_attr": "bold",
                "scale_color": {
                    2: "magenta",
                    4: "cyan"
                }
            }
        },
        {"scale": Scale("A", "major"), "chord": Chord("A#", "min")},
        (
            "  D  ║     |  E  |\x1b[38;5;3m\x1b[1m E#  \x1b[0m| F#  |\n"
            "\x1b[38;5;15m  A  \x1b[0m║\x1b[38;5;3m\x1b[1m A#  \x1b[0m|  B  |     |\x1b[38;5;3m\x1b[1m C#  \x1b[0m|\n"
            "  E  ║\x1b[38;5;3m\x1b[1m E#  \x1b[0m| F#  |     | G#  |\n"
            "\n"
            "  0  ║     |     |  3  |  4  |"
        )
    ),
    # Test with full standard tuning display #1 => E standard
    (
        E_STANDARD,
        {},
        {"scale": Scale("A", "major"), "chord": Chord("B", "dim7")},
        (
            "  E  ║  F  | F#  |     | Ab  |  A  |     |  B  |     | C#  |  D  |     |  E  |\n"
            "  B  ║     | C#  |  D  |     |  E  |  F  | F#  |     | Ab  |  A  |     |  B  |\n"
            "     ║ Ab  |  A  |     |  B  |     | C#  |  D  |     |  E  |  F  | F#  |     |\n"
            "  D  ║     |  E  |  F  | F#  |     | Ab  |  A  |     |  B  |     | C#  |  D  |\n"
            "  A  ║     |  B  |     | C#  |  D  |     |  E  |  F  | F#  |     | Ab  |  A  |\n"
            "  E  ║  F  | F#  |     | Ab  |  A  |     |  B  |     | C#  |  D  |     |  E  |\n"
            "\n"
            "  0  ║     |     |  3  |     |  5  |     |  7  |     |  9  |     |     | 12  |"
        )
    ),
    # Test with full standard tuning display #2 => E standard for bass
    (
        E_STANDARD_BASS,
        {},
        {"scale": Scale("A", "major"), "chord": Chord("B", "dim7")},
        (
            "     ║ Ab  |  A  |     |  B  |     | C#  |  D  |     |  E  |  F  | F#  |     |\n"
            "  D  ║     |  E  |  F  | F#  |     | Ab  |  A  |     |  B  |     | C#  |  D  |\n"
            "  A  ║     |  B  |     | C#  |  D  |     |  E  |  F  | F#  |     | Ab  |  A  |\n"
            "  E  ║  F  | F#  |     | Ab  |  A  |     |  B  |     | C#  |  D  |     |  E  |\n"
            "\n"
            "  0  ║     |     |  3  |     |  5  |     |  7  |     |  9  |     |     | 12  |"
        )
    ),
    # Test with full standard tuning display #3 => B standard
    (
        B_STANDARD_7,
        {},
        {"scale": Scale("A", "major"), "chord": Chord("B", "dim7")},
        (
            "  E  ║  F  | F#  |     | Ab  |  A  |     |  B  |     | C#  |  D  |     |  E  |\n"
            "  B  ║     | C#  |  D  |     |  E  |  F  | F#  |     | Ab  |  A  |     |  B  |\n"
            "     ║ Ab  |  A  |     |  B  |     | C#  |  D  |     |  E  |  F  | F#  |     |\n"
            "  D  ║     |  E  |  F  | F#  |     | Ab  |  A  |     |  B  |     | C#  |  D  |\n"
            "  A  ║     |  B  |     | C#  |  D  |     |  E  |  F  | F#  |     | Ab  |  A  |\n"
            "  E  ║  F  | F#  |     | Ab  |  A  |     |  B  |     | C#  |  D  |     |  E  |\n"
            "  B  ║     | C#  |  D  |     |  E  |  F  | F#  |     | Ab  |  A  |     |  B  |\n"
            "\n"
            "  0  ║     |     |  3  |     |  5  |     |  7  |     |  9  |     |     | 12  |"
        )
    ),
])
def test_fretboard_instanciation(tuning, fretboard_kwargs, call_kwargs, expected_ascii):
    fretboard = Fretboard(tuning, **fretboard_kwargs)

    assert fretboard.to_ascii(**call_kwargs) == expected_ascii
