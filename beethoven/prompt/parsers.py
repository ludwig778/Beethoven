from pyparsing import (CaselessLiteral, Group, Literal, Optional, Word,
                       ZeroOrMore, alphas, delimitedList, nums)

from beethoven.prompt.validator import (validate_chord, validate_note,
                                        validate_note_or_degree,
                                        validate_scale, validate_tempo,
                                        validate_time_signature)

alpha = Word(alphas)
alpha_note = Word(alphas + "#b")
integer = Word(nums)

#COMMAND_PARSER = CaselessLiteral("c=").suppress() + alpha("command")
COMMAND_PARSER = alpha("command")
SCALE_PARSER = (
    CaselessLiteral("sc=").suppress() + alpha("scale")
    .setParseAction(validate_scale)
)
NOTE_PARSER = (
    CaselessLiteral("n=").suppress() + alpha_note("note")
    .setParseAction(validate_note)
)
TEMPO_PARSER = (
    CaselessLiteral("t=").suppress() + integer("tempo")
    .setParseAction(validate_tempo)
)
TIME_SIGNATURE_PARSER = (
    CaselessLiteral("ts=").suppress() +
    (integer + Literal("/").suppress() + integer)("time_signature")
    .setParseAction(validate_time_signature)
)

CHORD_NAME_PARSER = (
    Word(alphas + nums + "#_")("chord")
    .setParseAction(validate_chord)
    # TODO
    # Should parse for note/degree
)
CHORD_INVERSION_PARSER = (
    CaselessLiteral(":i=").suppress() + integer("inversion")
    .setParseAction(lambda *args: int(args[2]["inversion"]))
)
CHORD_BASE_PARSER = (
    CaselessLiteral(":b=").suppress() + Word(alphas + "#b")("base")
    .setParseAction(validate_note_or_degree)
)
CHORD_DURATION_PARSER = (
    CaselessLiteral(":d=").suppress() +
    Optional(integer("duration_count")) + alpha("duration")
)

CHORD_PARSER = (
    CHORD_NAME_PARSER +
    Optional(CHORD_BASE_PARSER) +
    Optional(CHORD_DURATION_PARSER) +
    Optional(CHORD_INVERSION_PARSER)
)

PROGRESSION_PARSER = (
    CaselessLiteral("p=").suppress() +
    delimitedList(Group(CHORD_PARSER))("progression")
)

PARSER = delimitedList(Group(ZeroOrMore(
    SCALE_PARSER |
    NOTE_PARSER |
    TEMPO_PARSER |
    TIME_SIGNATURE_PARSER |
    PROGRESSION_PARSER |
    COMMAND_PARSER
)), delim=";")("harmony_list")
