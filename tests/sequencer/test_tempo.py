from pytest import mark

from beethoven.sequencer.tempo import Tempo


@mark.parametrize("tempo_arg", (30, 60, 120, 300))
def test_tempo_instanciation(tempo_arg):
    tempo = Tempo(tempo_arg)

    assert tempo

    assert repr(tempo) == f"<Tempo : {tempo_arg} bpm>"


def test_tempo_comparison():
    assert Tempo(30) == Tempo(30)

    assert Tempo(30) != Tempo(60)

    assert Tempo(30) < Tempo(60)

    assert Tempo(30) <= Tempo(30)

    assert Tempo(30) <= Tempo(60)
