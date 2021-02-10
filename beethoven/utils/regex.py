import re

INTERVAL_REGEX = r"(?P<interval_name>(\d{1,2}|[a-z]*))\ *"
INTERVAL_ALTERATION_REGEX = r"(?P<alteration>[M|m|a|d]*)"
CHORD_NAME_REGEX = r"(?P<chord_name>.*)"
DEGREE_REGEX = r"(?P<degree_name>((i|v){1,3}|(I|V){1,3}))"
NOTE_REGEX = r"(?P<note_name>([a-g]|[A-G]|(do|re|mi|fa|sol|la|si)|(Do|Re|Mi|Fa|Sol|La|Si)|(do|re|mi|fa|sol|la|si)))"
ALTERATION_REGEX = r"(?P<alteration>[#|b]*)"
OCTAVE_REGEX = r"(?P<octave>\d{1,2})"

INTERVAL_PARSER = re.compile(INTERVAL_REGEX + INTERVAL_ALTERATION_REGEX)
THEORY_NOTE_PARSER = re.compile(NOTE_REGEX + ALTERATION_REGEX)
SEQUENCER_NOTE_PARSER = re.compile(NOTE_REGEX + ALTERATION_REGEX + OCTAVE_REGEX)
HARMONY_PARSER = re.compile(DEGREE_REGEX + ALTERATION_REGEX + CHORD_NAME_REGEX)
