from pyparsing import ParseFatalException

from beethoven.sequencer.tempo import Tempo
from beethoven.sequencer.time_signature import TimeSignature
from beethoven.theory.chord import Chord
from beethoven.theory.harmony import Harmony
from beethoven.theory.note import Note
from beethoven.theory.scale import Scale


def handle_parser_exception(func):
    def wrapper(string, loc, expr):
        try:
            func(string, loc, expr)
        except Exception as exc:
            raise ParseFatalException(string, loc, str(exc))
    return wrapper


@handle_parser_exception
def validate_scale(string, loc, expr):
    Scale("A", expr[0])


@handle_parser_exception
def validate_note(string, loc, expr):
    Note(expr[0])


@handle_parser_exception
def validate_note_or_degree(string, loc, expr):
    try:
        Note(expr[0])
    except Exception:
        Harmony(Scale("A", "major")).get(expr[0])


@handle_parser_exception
def validate_tempo(string, loc, expr):
    Tempo(expr[0])


@handle_parser_exception
def validate_time_signature(string, loc, expr):
    TimeSignature(*expr)


@handle_parser_exception
def validate_chord_item(string, loc, expr):
    value = expr[0].replace("_", " ")

    if not (
        Chord.get_from_fullname(value) or
        Harmony(Scale("A", "major")).get(value)
    ):
        raise Exception("Couldn't parse chord item")
