from pytest import raises

from beethoven.sequencer.players.base import BasePlayer, Players


class FakePlayer1(BasePlayer):
    pass


class FakePlayer2(BasePlayer):
    pass


def test_players_instanciation():
    players = Players(FakePlayer1)

    assert repr(players) == "<Players : 1 players>"

    players.add(FakePlayer1)

    assert repr(players) == "<Players : 2 players>"
    assert len(players.all()) == 2

    assert players.all() == {
        0: FakePlayer1,
        1: FakePlayer1
    }
    assert Players.get("FakePlayer1").__class__ == FakePlayer1

    players.remove(1)
    assert players.all() == {0: FakePlayer1}

    players.update({
        0: FakePlayer2
    })
    assert players.all() == {0: FakePlayer2}


def test_players_instanciation_exception():
    players = Players()
    for _ in range(players.MAX_CHANNELS):
        players.add(FakePlayer1)

    with raises(Exception, match="All channels taken by players"):
        players.add(FakePlayer1)
