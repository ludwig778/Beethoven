from beethoven.ui.components.selectors.multiple.base import MultipleSelector
from beethoven.ui.constants import NOTE_LABELS, NOTES_DATA, SELECTED_NOTE_LABELS


class MultipleNoteSelector(MultipleSelector):
    def __init__(self, *args, **kwargs):
        super(MultipleNoteSelector, self).__init__(
            *args,
            data=NOTES_DATA,
            labels=NOTE_LABELS,
            expanded_labels=SELECTED_NOTE_LABELS,
            checked_labels=SELECTED_NOTE_LABELS,
            **kwargs
        )

        self.notes = {
            str(note): note for _, notes in NOTES_DATA.items() for note in notes
        }

    def get_checked_notes(self):
        return [self.notes[item_text] for item_text in self.get_checked_texts()]
