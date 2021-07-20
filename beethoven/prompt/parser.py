from collections import defaultdict

from pyparsing import (CaselessLiteral, Group,
                       Optional, Suppress, Word, ZeroOrMore, alphas,
                       delimitedList, nums, printables)

from beethoven.models import GridPart as GridPartModel
from beethoven.prompt.validator import (validate_chord_item, validate_note,
                                        validate_scale, validate_tempo,
                                        validate_time_signature)
from beethoven.sequencer.grid import Grid, GridPart
from beethoven.sequencer.note_duration import (Eighths, Half, Quarter,
                                               Sixteenths, Whole)
from beethoven.sequencer.tempo import Tempo
from beethoven.sequencer.time_signature import TimeSignature
from beethoven.theory.chord import Chord
from beethoven.theory.harmony import Harmony
from beethoven.theory.scale import Scale

alpha = Word(alphas)
integer = Word(nums)
all_printables = Word(printables + " ")

command = Word(alphas + nums + "#.,:=_+-Δ°ø()")


class Base:
    def __init__(self, tokens, **kw):
        self.tokens = tokens
        if getattr(self, "post_init", None):
            self.post_init()
        if getattr(self, "validate", None):
            self.validate()

    @property
    def value(self):
        if len(self.tokens) == 1:
            return self.tokens[0]
        return ' '.join(map(str, self.tokens))

    def token_labels(self):
        return [getattr(t, "label", None) for t in self.tokens]

    def expand_values(self, **kwargs):
        return self.eval_tokens(self.tokens, **kwargs)

    @staticmethod
    def filter_tokens(tokens, *token_class):
        return [t for t in tokens if isinstance(t, token_class)]

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.value}>"

    @classmethod
    def eval_tokens(cls, tokens, **kwargs):
        return [
            t.eval(**kwargs) if isinstance(t, Base) else t
            for t in tokens
        ]


class MainParser(Base):
    def __init__(self, tokens, **kwargs):
        super().__init__(tokens, **kwargs)

        if progression_token := self.filter_tokens(self.tokens, ProgressionParser):
            progression_string = progression_token[0].eval()
            full_progression_token = full_compose_items.parseString(progression_string)[0]
            self.tokens.append(full_progression_token)

    def eval(self, **kwargs):
        token_by_labels = dict(zip(self.token_labels(), self.tokens))

        parts = []
        if parts_token := token_by_labels.get("parts"):
            parts = parts_token.eval(**kwargs)

        return Grid(parts)


class MainCommandParser(Base):
    label = "main_command"

    def eval(self, **kwargs):
        return self.expand_values()[0]


class ProgressionParser(Base):
    label = "raw"

    def eval(self, **kwargs):
        return self.expand_values(**kwargs)[0]


class ScaleParser(Base):
    label = "scale_name"

    def validate(self):
        validate_scale(self.value)

    def eval(self, **kwargs):
        return self.expand_values()[0]


class NoteParser(Base):
    label = "scale_note"

    def validate(self):
        validate_note(self.value)

    def eval(self, **kwargs):
        return self.expand_values()[0]


class TempoParser(Base):
    label = "tempo"

    def validate(self):
        validate_tempo(self.value)

    def eval(self, **kwargs):
        return Tempo(int(self.expand_values()[0]))


class TimeSignatureParser(Base):
    label = "time_signature"

    def post_init(self):
        self.tokens = self.tokens[0]

    @property
    def value(self):
        return "/".join(self.tokens)

    def validate(self):
        validate_time_signature(*self.tokens)

    def eval(self, **kwargs):
        return TimeSignature(*self.expand_values())


class RepeatParser(Base):
    label = "repeat"

    def eval(self, **kwargs):
        return int(self.expand_values()[0])


class BypassParser(Base):
    label = "bypass"

    @property
    def value(self):
        return self.tokens[0] == "!"

    def eval(self, **kwargs):
        return self.expand_values()[0] == "!"


class CommandParser(Base):
    label = "command"

    def eval(self, **kwargs):
        return self.expand_values()[0]


class ProgressionItemParser(Base):
    def post_init(self):
        self.tokens = self.tokens[0]

    def eval(self, **kwargs):
        config = kwargs.get("config") or {}
        values = {}

        token_by_labels = dict(zip(self.token_labels(), self.tokens))
        current_scale = config.get("scale")
        if "scale_name" in token_by_labels or "scale_note" in token_by_labels:
            new_scale = None

            scale_name = None
            scale_note = None

            if scale_name_parser := token_by_labels.pop("scale_name", None):
                scale_name = scale_name_parser.eval()
            if scale_note_parser := token_by_labels.pop("scale_note", None):
                scale_note = scale_note_parser.eval()

            if current_scale and (current_scale.name != scale_name or current_scale.tonic.name != scale_note):
                new_scale = Scale(
                    scale_note or current_scale.tonic.name,
                    scale_name or str(current_scale.name)
                )
                config["scale"] = new_scale
                values["scale"] = new_scale

                current_scale = new_scale
            elif scale_name and scale_note:
                new_scale = Scale(
                    scale_note,
                    scale_name
                )
                config["scale"] = new_scale
                values["scale"] = new_scale

                current_scale = new_scale

        if not current_scale:
            return []
        else:
            values["scale"] = current_scale

        values.update({
            k: v.eval(**kwargs)
            for k, v in token_by_labels.items()
        })

        config["chords"] = values.get("chords") or []

        values.setdefault("time_signature", config.get("time_signature"))
        values.setdefault("tempo", config.get("tempo"))
        values.setdefault("scale", config.get("scale"))

        return [
            GridPart(chord=chord, duration=duration, **values)
            for chord, duration in values.pop("chords")
        ]


class ChordProgressionParser(Base):
    label = "chords"

    def eval(self, **kwargs):
        return self.expand_values(**kwargs)


class FullProgressionParser(Base):
    label = "parts"

    def eval(self, **kwargs):
        sub_parts = self.expand_values(**kwargs)

        return [part for parts in sub_parts for part in parts]


class ChordParser(Base):
    def eval(self, **kwargs):
        values = defaultdict(list)

        for k, v in zip(self.token_labels(), self.expand_values(**kwargs)):
            if k == "extensions":
                values[k].append(v)
            else:
                values[k] = v

        duration = values.pop("duration", None)

        scale = kwargs.get("config", {}).get("scale")

        base_degree = None
        if values.get("base_note") and values.get("base_note").lower() in ("i", "ii", "iii", "iv", "v", "vi", "vii"):
            base_degree = values.pop("base_note")

        chord_name = values.pop("name")

        if not (chord := Harmony(scale).get(chord_name, base_degree=base_degree, **values)):
            chord = Chord.get_from_fullname(chord_name, **values)

        return chord, duration


class ChordNameParser(Base):
    label = "name"

    def post_init(self):
        self.tokens[0] = self.tokens[0].replace("_", " ")

    def validate(self):
        validate_chord_item(self.tokens[0])

    def eval(self, **kwargs):
        return self.expand_values()[0]


class ChordBaseParser(Base):
    label = "base_note"

    def eval(self, **kwargs):
        return self.expand_values()[0]


class ChordDurationParser(Base):
    label = "duration"
    mapping = {
        "H": Half,
        "W": Whole,
        "Q": Quarter,
        "E": Eighths,
        "S": Sixteenths
    }

    def eval(self, **kwargs):
        value = list(self.expand_values()[0])
        identifier = value.pop(-1)
        duration = self.mapping.get(identifier)
        if value:
            num = int(value.pop())
            duration *= num
        return duration


class ChordInversionParser(Base):
    label = "inversion"

    def eval(self, **kwargs):
        return int(self.expand_values()[0])


class ChordExtentionsParser(Base):
    label = "extensions"

    def eval(self, **kwargs):
        return self.expand_values()[0]


scale_pattern = Word(alphas + nums + "#_-")
note_pattern = Word(alphas + "#b")
degree_pattern = Word("IV") + Word("#bad")
tempo_pattern = integer
time_signature_pattern = Group(integer + Suppress("/") + integer)
repeat_pattern = integer
bypass_pattern = CaselessLiteral("!")
command_pattern = Word(alphas + nums + "._")

chord_name_pattern = Word(alphas + nums + "#_+-Δ°ø()")
chord_base_pattern = Word(alphas + "#b")
chord_duration_pattern = Group(Optional(integer) + Word(alphas))
chord_inversion_pattern = integer
chord_extensions_pattern = Word(alphas + nums)

scale = (Suppress("sc=") + scale_pattern).setParseAction(ScaleParser)
note = (Suppress("n=") + note_pattern).setParseAction(NoteParser)
tempo = (Suppress("t=") + tempo_pattern).setParseAction(TempoParser)
time_signature = (Suppress("ts=") + time_signature_pattern).setParseAction(TimeSignatureParser)
repeat = (Suppress("r=") + repeat_pattern).setParseAction(RepeatParser)
bypass = bypass_pattern.setParseAction(BypassParser)
command = command_pattern.setParseAction(CommandParser)

chord_name = chord_name_pattern.setParseAction(ChordNameParser)
chord_base = (Suppress(":b=") + chord_base_pattern).setParseAction(ChordBaseParser)
chord_duration = (Suppress(":d=") + chord_duration_pattern).setParseAction(ChordDurationParser)
chord_inversion = (Suppress(":i=") + chord_inversion_pattern).setParseAction(ChordInversionParser)
chord_extensions = (Suppress(":e=") + chord_extensions_pattern).setParseAction(ChordExtentionsParser)
chord = (
    chord_name + ZeroOrMore(
        chord_base |
        chord_duration |
        chord_inversion |
        chord_extensions
    )
).setParseAction(ChordParser)

progression_pattern = Optional(delimitedList(
    chord,
    delim=","
))
progression = (
    (Suppress("p=") + progression_pattern)
).setParseAction(ChordProgressionParser)

compose_item = Group(
    ZeroOrMore(
        scale | note | tempo | time_signature | repeat | bypass | progression | command
    )
).setParseAction(ProgressionItemParser)

compose_items = all_printables.addParseAction(ProgressionParser)
full_compose_items = Optional(delimitedList(compose_item, delim=";")).addParseAction(FullProgressionParser)

info, delete, settings, register = map(
    lambda x: CaselessLiteral(x).setParseAction(MainCommandParser),
    ("info", "delete", "settings", "register")
)

commands = Optional(
    info + ZeroOrMore(command) |
    delete + command |
    settings |
    Optional(register + command) + compose_items
).setParseAction(MainParser)

COMPOSE_PARSER = None
SECTION_PARSER = None


def prompt_harmony_list_parser(string, config=None):
    if config is None:
        config = {}

    ppp = commands.parseString(string)
    evaluated = ppp[0].eval(config=config)

    return evaluated
