from prompt_toolkit.completion import WordCompleter

from beethoven.prompt.base import BasePrompt
from beethoven.prompt.display import display
from beethoven.prompt.parser import prompt_harmony_list_parser
from beethoven.prompt.state import state
from beethoven.sequencer.grid import Grid


class ComposePrompt(BasePrompt):
    PROMPT_STR = "compose> "

    def _get_completer(self):
        return WordCompleter([])

    def _help(self):
        print(" == Composer ==")
        print(" Define as much parts as you want, semi colon separated")
        print()
        print(" Each parts are defined with the following attributes")
        print("   scale with sc=major")
        print("   note with n=C#")
        print("   tempo with t=90")
        print("   time signature with ts=5/4")
        print("   progression with p=II,V,I")
        print()
        print(" Progression is a comma separated list of degrees or chords")
        print(" Could be:")
        print("   p=I,IV,V")
        print("   p=Amaj7,C#min7,E7")
        print()

    def dispatch(self, text):
        try:
            grid = Grid(parts=prompt_harmony_list_parser(text, full_config=state.config))

            state.jam_room.grid = grid
            state.jam_room.play(callback=display)

        except ValueError as exc:
            print(f"Error : {str(exc)}")
            return
