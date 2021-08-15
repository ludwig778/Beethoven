from pytest import mark

from beethoven.objects import TimeSignature
from beethoven.utils.factory import factory


@mark.parametrize("string,time_signature", [
    ("4/4",   TimeSignature(4, 4)),
    ("3/2",   TimeSignature(3, 2)),
    ("12/8",  TimeSignature(12, 8)),
    ("15/16", TimeSignature(15, 16)),
])
def test_time_signature_parsing(string, time_signature):
    assert factory("time_signature", string) == time_signature
