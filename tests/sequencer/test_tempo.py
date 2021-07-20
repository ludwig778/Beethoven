from beethoven.sequencer.tempo import Tempo


def test_tempo_instanciation():
    assert Tempo(30)


def test_tempo_comparison():
    assert Tempo(30) == Tempo(30)

    assert Tempo(30) != Tempo(60)

    assert Tempo(30) < Tempo(60)

    assert Tempo(30) <= Tempo(30)

    assert Tempo(30) <= Tempo(60)
