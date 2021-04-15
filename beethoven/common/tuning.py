from beethoven.theory.note import Note


class Tuning:
    def __init__(self, *strings):
        self.strings = list(strings)

    def __eq__(self, other):
        return self.strings == other.strings

    def __str__(self):
        return f"<Tuning {len(self.strings)} strings>"

    def __repr__(self):
        return str(self)


E_STANDARD = Tuning(*Note.to_list("E,A,D,G,B,E"))
E_STANDARD_BASS = Tuning(*Note.to_list("E,A,D,G"))
B_STANDARD_7 = Tuning(*Note.to_list("B,E,A,D,G,B,E"))
