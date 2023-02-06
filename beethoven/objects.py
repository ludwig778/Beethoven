from beethoven.constants import duration as duration_constants
from beethoven.models import Duration, Interval

octave = Interval(name="8")

whole_duration = Duration(value=duration_constants.whole_value)
half_duration = Duration(value=duration_constants.half_value)
quarter_duration = Duration(value=duration_constants.quarter_value)
eighth_duration = Duration(value=duration_constants.eighth_value)
sixteenth_duration = Duration(value=duration_constants.sixteenth_value)
