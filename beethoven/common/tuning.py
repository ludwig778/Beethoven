from beethoven.theory.note import Note


class Tuning:
    def __init__(self, *strings):
        self.strings = list(strings)

    def __str__(self):
        return f"<Tuning {len(self.strings)} strings>"

    def __repr__(self):
        return str(self)

    @classmethod
    def from_notes_str(cls, string):
        return cls(*Note.to_list(string))


E_STANDARD = Tuning(*Note.to_list("E,A,D,G,B,E"))
E_STANDARD_BASS = Tuning(*Note.to_list("E,A,D,G"))
B_STANDARD_7 = Tuning(*Note.to_list("B,E,A,D,G,B,E"))
