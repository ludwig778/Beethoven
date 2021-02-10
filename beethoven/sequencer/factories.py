from .tempo import Tempo
from .time_signature import TimeSignature


def default_tempo_factory():
    return Tempo()


def default_time_signature_factory():
    return TimeSignature()
