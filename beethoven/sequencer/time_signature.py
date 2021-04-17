from beethoven.sequencer.note_duration import Quarter


class TimeSignature:
    DEFAULT_BEAT_UNIT = 4
    DEFAULT_BEATS_PER_BAR = 4

    def __init__(self, beat_unit=None, beats_per_bar=None):
        self.set(
            beat_unit or self.DEFAULT_BEAT_UNIT,
            beats_per_bar or self.DEFAULT_BEATS_PER_BAR
        )

    def set(self, beat_unit=None, beats_per_bar=None):
        if beat_unit:
            self.beat_unit = int(beat_unit)
        if beats_per_bar:
            self.beats_per_bar = int(beats_per_bar)

    def copy(self):
        return self.__class__(self.beat_unit, self.beats_per_bar)

    def __repr__(self):
        return f"<Time Signature : {str(self)}>"

    def __str__(self):
        return f"{self.beat_unit}/{self.beats_per_bar}"

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.beat_unit == other.beat_unit and
            self.beats_per_bar == other.beats_per_bar
        )

    def duration(self, tempo):
        reduction = self.beats_per_bar / 4

        quarter = Quarter.duration(bpm=tempo)

        return (self.beat_unit * quarter) / reduction

    def gen(self, *args, **kwargs):
        return self._gen(*args, **kwargs)

    def _get_time_section(self, count, divisor, beats_per_bar=None, beat_unit=None):
        raw_submeasure, divisor_index = divmod(count, divisor)
        raw_measure, submeasure = divmod(raw_submeasure, beats_per_bar or self.beats_per_bar)
        bar, measure = divmod(raw_measure, beat_unit or self.beat_unit)

        return TimeContainer(
            bar + 1,
            measure + 1,
            submeasure + 1,
            divisor_index + 1,
            divisor
        )

    def normalize_part(self, part):
        ratio = self.beats_per_bar / 4
        divisor = part.divisor

        raw_measure = ((part.bar - 1) * self.beat_unit) + (part.measure - 1)
        raw_submeasure = (raw_measure * self.beats_per_bar) + (part.submeasure - 1)
        count = ((part.divisor * raw_submeasure) - 1) + (part.divisor_index)

        while True:
            if divisor % 2:
                break

            divisor = int(divisor / 2)
            count = count / 2

        count = int(count / (ratio ** 2))

        return self._get_time_section(
            count,
            divisor,
            beats_per_bar=4,
            beat_unit=int(self.beat_unit / ratio)
        )

    def _gen(self, note_duration, duration=None, go_on=False):
        reduction = self.beats_per_bar / 4

        divisor = note_duration.divisor
        reduc_ratio = self.beats_per_bar * reduction

        while not (divisor % 2 or reduc_ratio % 2):
            divisor //= 2
            reduc_ratio //= 2

        base_units = int(note_duration.base_units * reduc_ratio)

        # Get total duration
        if duration:
            last_section = self._get_time_section(
                int(duration.base_units * self.beats_per_bar * reduction * divisor / duration.divisor),
                divisor
            )
        elif go_on:
            last_section = None
        else:
            last_section = self._get_time_section(
                self.beat_unit * self.beats_per_bar * divisor,
                divisor
            )

        count = 0
        while 1:
            time_section = self._get_time_section(count, divisor)

            if last_section is not None and last_section <= time_section:
                return

            """
            if normalize_part:
                yield self.normalize_part(time_section)
            else:
            """
            yield time_section

            count += base_units


class TimeContainer:
    def __init__(self, bar, measure, submeasure, divisor_index=1, divisor=1):
        self.bar = bar
        self.measure = measure
        self.submeasure = submeasure
        self.divisor_index = divisor_index
        self.divisor = divisor

    def check(self, **kwargs):
        checks = []
        for k, v in kwargs.items():
            self_value = getattr(self, k)
            if isinstance(v, int):
                checks.append(self_value == v)
            else:
                checks.append(self_value in v)

        return all(checks)

    def copy(self):
        return self.__class__(self.bar, self.measure, self.submeasure, self.divisor_index, self.divisor)

    def __repr__(self):
        return f"<Time {self.bar} | {self.measure} / {self.submeasure} ( {self.divisor_index} : {self.divisor} )>"

    def __eq__(self, other):
        return (
            self.bar == other.bar and
            self.measure == other.measure and
            self.submeasure == other.submeasure and
            self.divisor_index == other.divisor_index and
            self.divisor == other.divisor
        )

    def __lt__(self, other):
        if self.bar < other.bar:
            return True
        elif self.bar > other.bar:
            return False

        if self.measure < other.measure:
            return True
        elif self.measure > other.measure:
            return False

        if self.submeasure < other.submeasure:
            return True
        elif self.submeasure > other.submeasure:
            return False

        return (
            self.divisor_index / self.divisor <
            other.divisor_index / other.divisor
        )

    def __le__(self, other):
        return self == other or self < other

    def start_offset(self, time_signature, tempo):
        reduction = time_signature.beats_per_bar / 4

        quarter = Quarter.duration(bpm=tempo) / reduction

        beats_per_bar = time_signature.beats_per_bar
        beat_unit = time_signature.beat_unit

        bar_part = (self.bar - 1) * beat_unit
        measure_part = self.measure - 1
        submeasure_part = (self.submeasure - 1) / beats_per_bar
        divisor_part = (1 / beats_per_bar) * ((self.divisor_index - 1) / self.divisor)

        return (bar_part + measure_part + submeasure_part + divisor_part) * quarter
