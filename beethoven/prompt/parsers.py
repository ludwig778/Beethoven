from pyparsing import (CaselessLiteral, Group, Literal, Optional, Word,
                       ZeroOrMore, alphas, delimitedList, nums)

from beethoven.prompt.validator import (validate_chord_item, validate_note,
                                        validate_note_or_degree,
                                        validate_scale, validate_tempo,
                                        validate_time_signature)

alpha = Word(alphas)
alpha_note = Word(alphas + "#b")
integer = Word(nums)

command = Word(alphas + nums + "#.,:=_+-Δ°ø()")

REGISTER_PARSER = CaselessLiteral("register").suppress() + command("register")
INFO_PARSER = CaselessLiteral("info").suppress() + Group(ZeroOrMore(command))("info")
DELETE_PARSER = CaselessLiteral("delete").suppress() + command("delete")
SETTINGS_PARSER = CaselessLiteral("settings")("settings").setParseAction(lambda *a: True)
COMMAND_PARSER = command("command")
SCALE_PARSER = (
    CaselessLiteral("sc=").suppress() + Word(alphas + nums + "#_-")("scale")
    .addParseAction(lambda v: v[0].replace("_", " "))
    .addParseAction(validate_scale)
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
REPEAT_PARSER = (
    (
        CaselessLiteral("r=") |
        CaselessLiteral("repeat=")
    ).suppress() +
    integer("repeat")
    .setParseAction(lambda v: int(v[0]))
)
BYPASS_PARSER = (
    CaselessLiteral("!")("bypass")
    .setParseAction(lambda *a: True)
)

CHORD_NAME_PARSER = (
    Word(alphas + nums + "#_+-Δ°ø()")("chord")
    .addParseAction(lambda v: v[0].replace("_", " "))
    .addParseAction(validate_chord_item)
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
CHORD_EXTENSIONS_PARSER = ZeroOrMore(
    CaselessLiteral(":e=").suppress() +
    Word(alphas + nums).setResultsName("extensions", listAllMatches=True)
)

CHORD_PARSER = (
    CHORD_NAME_PARSER +
    (
        Optional(CHORD_BASE_PARSER) &
        Optional(CHORD_DURATION_PARSER) &
        Optional(CHORD_INVERSION_PARSER) &
        Optional(CHORD_EXTENSIONS_PARSER)
    )
)

PROGRESSION_PARSER = (
    CaselessLiteral("p=").suppress() +
    Optional(delimitedList(Group(CHORD_PARSER)))("progression")
)

SECTION_PARSER = ZeroOrMore(
    SCALE_PARSER |
    NOTE_PARSER |
    TEMPO_PARSER |
    TIME_SIGNATURE_PARSER |
    PROGRESSION_PARSER |
    REPEAT_PARSER |
    BYPASS_PARSER |
    COMMAND_PARSER
)

HARMONY_STRINGS_PARSER = ZeroOrMore(delimitedList(
    Word(alphas + nums + "()#_=/:, !.+-Δ°ø"),
    delim=";"
))

COMPOSE_PARSER = (
    INFO_PARSER |
    DELETE_PARSER |
    SETTINGS_PARSER |
    (
        Optional(REGISTER_PARSER) +
        HARMONY_STRINGS_PARSER("harmony_strings")
    )
)
