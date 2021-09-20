import re

INTERVAL_REGEX = r"(?P<interval_name>(\d{1,2}|[a-z]*))\ *"
INTERVAL_ALTERATION_REGEX = r"(?P<alteration>[M|m|a|d]*)"
CHORD_NAME_REGEX = r"(?P<chord_name>.*)"
DEGREE_REGEX = r"(?P<degree_name>((i|v){1,3}|(I|V){1,3}))"
NOTE_REGEX = (
    r"(?P<note_name>((Do|Ré|Mi|Fa|Sol|La|Si)|(do|re|ré|mi|fa|sol|la|si)|[A-G]{1}))"
)
ALTERATION_REGEX = r"(?P<alteration>[#|b]*)"
OCTAVE_REGEX = r"(?P<octave>\d{1})"

INTERVAL_PARSER = re.compile(INTERVAL_REGEX + INTERVAL_ALTERATION_REGEX)
THEORY_NOTE_PARSER = re.compile(NOTE_REGEX + ALTERATION_REGEX)
HARMONY_PARSER = re.compile(ALTERATION_REGEX + DEGREE_REGEX + CHORD_NAME_REGEX)
CHORD_PARSER = re.compile(NOTE_REGEX + ALTERATION_REGEX + CHORD_NAME_REGEX)

SEQUENCER_NOTE_PARSER = re.compile(NOTE_REGEX + ALTERATION_REGEX + OCTAVE_REGEX)
SEQUENCER_CHORD_PARSER = re.compile(
    NOTE_REGEX + ALTERATION_REGEX + OCTAVE_REGEX + CHORD_NAME_REGEX
)

PROGRESSION_ENTRY_PARSER = re.compile(r"(?<=(p|P)=)(?P<progression>.*)")
NOTE_ENTRY_PARSER = re.compile(
    r"((?<=(n|N)=)|(?<=(note|NOTE)=))(?P<note>[A-Za-z0-9#b]+)"
)
SCALE_ENTRY_PARSER = re.compile(
    r"((?<=(sc|SC)=)|(?<=(scale|SCALE)=))(?P<scale>[a-z_]*)"
)
TEMPO_ENTRY_PARSER = re.compile(r"((?<=(t|T)=)|(?<=(bpm|BPM)=))(?P<tempo>\d*)")
TIME_SIGNATURE_ENTRY_PARSER = re.compile(
    r"((?<=(ts|TS)=)|(?<=(sig|SIG)=))(?P<time_signature>[0-9/]*)"
)
FLAG_ENTRY_PARSER = re.compile(
    r"((?<=(f|F)=)|(?<=(flag|FLAG)=))(?P<flag>[A-Za-z0-9-_|]*)"
)
PROMPT_ENTRY_PARSERS = {
    "progression": PROGRESSION_ENTRY_PARSER,
    "note": NOTE_ENTRY_PARSER,
    "scale": SCALE_ENTRY_PARSER,
    "tempo": TEMPO_ENTRY_PARSER,
    "time_signature": TIME_SIGNATURE_ENTRY_PARSER,
    "flag": FLAG_ENTRY_PARSER,
}
