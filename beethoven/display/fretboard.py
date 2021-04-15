from colored import attr, fg


class Fretboard:
    def __init__(self, tuning, first_fret=None, last_fret=12, config=None):
        self.tuning = tuning

        self.first_fret = first_fret or 0
        self.last_fret = last_fret

        self.config = config or {}

    @staticmethod
    def _get_notes_semitones(obj):
        if not obj:
            return {}

        return {
            note.semitones: note
            for note in obj.notes
        }

    def to_ascii(self, scale=None, chord=None, first_fret=None, last_fret=None):  # noqa: C901
        first_fret = first_fret or self.first_fret
        last_fret = last_fret or self.last_fret

        chord_semitones = self._get_notes_semitones(chord)
        scale_semitones = self._get_notes_semitones(scale)

        all_semitones = {**chord_semitones, **scale_semitones}

        fretboard_strings = []

        for string in self.tuning.strings[::-1]:
            string_display = ""
            for fret in range(first_fret or 0, last_fret + 1):
                attr_name = None
                color = None

                note_semitones = (string.semitones + fret) % 12
                note = all_semitones.get(note_semitones)

                if scale and note_semitones in scale_semitones:
                    scale_note = scale_semitones.get(note_semitones)

                    color = (
                        self.config
                        .get("diatonic_color" if len(scale_semitones) == 7 else "scale_color", {})
                        .get(scale.notes.index(scale_note))
                    )

                if chord and note_semitones in chord_semitones:
                    note = chord_semitones.get(note_semitones)

                    if color := self.config.get("chord_color"):
                        pass

                    if attr_name := self.config.get("chord_attr"):
                        pass

                if scale and note and note == scale.notes[0]:
                    color = self.config.get("tonic_color")

                if color:
                    string_display += fg(color)
                if attr_name:
                    string_display += attr(attr_name)

                string_display += "{:^5}".format(note.name) if note else " " * 5

                if color or attr_name:
                    string_display += attr("reset")

                string_display += '║' if fret == 0 else '|'

            fretboard_strings.append(string_display)

        fretboard_strings.append("")

        fret_display = ""
        for fret in range(first_fret or 0, last_fret + 1):
            fret_display += "{:^5}".format(fret if (
                fret % 12 in (0, 3, 5, 7, 9) or
                fret in (first_fret or 0, last_fret)
            ) else "")

            fret_display += '║' if fret == 0 else '|'

        fretboard_strings.append(fret_display)

        return "\n".join(fretboard_strings)
