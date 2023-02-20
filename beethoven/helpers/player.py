from typing import List, Tuple

from beethoven.sequencer.players import BasePlayer


def split_player_by_types(
    players: List[BasePlayer],
) -> Tuple[List[BasePlayer], List[BasePlayer]]:
    regular = []
    time_signature_bound = []

    for player in players:
        if player.time_signature_bound:
            time_signature_bound.append(player)
        else:
            regular.append(player)

    return regular, time_signature_bound
