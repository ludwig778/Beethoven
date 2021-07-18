from beethoven.sequencer.tempo import Tempo
from beethoven.sequencer.time_signature import TimeSignature
from beethoven.theory.chord import Chord
from beethoven.theory.harmony import Harmony
from beethoven.theory.note import Note
from beethoven.theory.scale import Scale


class ValidationError(ValueError):
    pass


def handle_parser_exception(func):
    def wrapper(*args):
        try:
            func(*args)
        except Exception as exc:
            raise ValidationError(f"Parsing validation error: {str(exc)}")
    return wrapper


@handle_parser_exception
def validate_scale(name):
    Scale("A", name)


@handle_parser_exception
def validate_note(name):
    Note(name)


@handle_parser_exception
def validate_note_or_degree(string, loc, expr):
    try:
        Note(expr[0])
    except Exception:
        Harmony(Scale("A", "major")).get(expr[0])


@handle_parser_exception
def validate_tempo(num):
    Tempo(num)


@handle_parser_exception
def validate_time_signature(beat, per_bar):
    TimeSignature(beat, per_bar)


@handle_parser_exception
def validate_chord_item(item):
    if not (
        Chord.get_from_fullname(item) or
        Harmony(Scale("A", "major")).get(item)
    ):
        raise Exception("Couldn't parse chord item")
