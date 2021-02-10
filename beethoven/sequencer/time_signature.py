from beethoven.sequencer.note_duration import Quarter


class TimeSignature:
    DEFAULT_BEAT_UNIT = 4
    DEFAULT_BEATS_PER_BAR = 4

    def __init__(self, beat_unit=None, beats_per_bar=None):
        self.set(
            beat_unit or self.DEFAULT_BEAT_UNIT,
            beats_per_bar or self.DEFAULT_BEATS_PER_BAR
        )

    def reset(self):
        self.set(
            self.DEFAULT_BEAT_UNIT,
            self.DEFAULT_BEATS_PER_BAR
        )

    def set(self, beat_unit, beats_per_bar):
        self.beat_unit = beat_unit
        self.beats_per_bar = beats_per_bar

    def get(self):
        return self.value

    def copy(self):
        return self.__class__(self.beat_unit, self.beats_per_bar)

    def __repr__(self):
        return f"<Time Signature : {self.beat_unit}/{self.beats_per_bar}>"

    def __eq__(self, other):
        return (
            self.beat_unit == other.beat_unit and
            self.beats_per_bar == other.beats_per_bar
        )

    def get_duration(self, tempo):
        reduction = self.beats_per_bar / 4

        quarter = Quarter.duration(bpm=tempo)

        return (self.beat_unit * quarter) / reduction

    def gen(self, *args, **kwargs):
        return self._gen(*args, **kwargs)

    def _gen(self, note_duration, duration=None, go_on=False):
        reduction = self.beats_per_bar / 4

        single_computed_time = (1 * note_duration.base_units) / (note_duration.divisor / reduction)
        divisions = note_duration.divisor
        
        # REMOVE THAT
        if duration:
            total_duration = duration.base_units / reduction
        else:
            total_duration = self.beat_unit

        count = 0
        while 1:
            computed = count * single_computed_time
            measure, submeasure_rest = divmod(computed, 1)
            measure = int(measure + 1)

            if computed >= total_duration:
                break

            raw_submeasure = submeasure_rest * self.beats_per_bar
            submeasure = int(raw_submeasure) + 1
            divisor_index = int(((((raw_submeasure % 1) * reduction) * note_duration.base_units) / single_computed_time) + 1.0000001)

            print(f"----{computed:3.3f} {total_duration:3d}")
            print(
                " - -----  "
                f"{raw_submeasure:3.3f} "
                f"{(raw_submeasure % 1):3.3f} "
                f"{(raw_submeasure % 1) / single_computed_time:3.3f} "
                f"{(raw_submeasure % 1) / (single_computed_time / note_duration.base_units):3.3f} "
                f"{divisor_index:3.3f}"
            )
            """
            """

            yield TimeContainer(measure, submeasure, int(divisor_index), divisions)

            count += 1


class TimeContainer:
    def __init__(self, measure, submeasure, divisor_index=1, divisor=1, max_time=None):
        self.measure = measure
        self.submeasure = submeasure
        self.divisor_index = divisor_index
        self.divisor = divisor
        self.max_time = max_time

    def check(self, measure=None, submeasure=None, divisor_index=None):
        return (
            (
                not measure or (
                    self.measure == measure
                    if isinstance(measure, int)
                    else self.measure in measure
                )
            ) and
            (
                not submeasure or (
                    self.submeasure == submeasure
                    if isinstance(submeasure, int)
                    else self.submeasure in submeasure
                )
            ) and
            (
                not divisor_index or (
                    self.divisor_index == divisor_index
                    if isinstance(divisor_index, int)
                    else self.divisor_index in divisor_index
                )
            )
        )

    def copy(self):
        return self.__class__(self.measure, self.submeasure, self.divisor_index, self.divisor)

    def __repr__(self):
        return f"<Time {self.measure} / {self.submeasure} ( {self.divisor_index} : {self.divisor}) >"

    def __eq__(self, other):
        return (
            self.measure == other.measure and
            self.submeasure == other.submeasure and
            self.divisor_index == other.divisor_index and
            self.divisor == other.divisor
        )

    def __lt__(self, other):
        a = (self.divisor_index) / self.divisor
        b = (other.divisor_index) / other.divisor

        print(a, b)
        print(a < b)
        return (
            self.measure < other.measure or (
                self.measure == other.measure and
                self.submeasure < other.submeasure or (
                    self.measure == other.measure and
                    self.submeasure == other.submeasure and
                    a < b
                )
            )
        )

    def start_offset(self, time_signature, tempo):
        reduction = time_signature.beats_per_bar / 4

        quarter = Quarter.duration(bpm=tempo)
        print()

        #print(self.__dict__, quarter, reduction)
        lmao = (
            #(((self.submeasure - 1) * quarter) / reduction) + \
            ((self.measure - 1) * quarter) / reduction) + \
            ((((self.divisor_index - 1) / self.divisor) * quarter) / reduction
        )
        print("---", self, quarter, lmao)
        #print((((self.measure - 1) * quarter) / reduction) + (((self.divisor_index / self.divisor) * quarter) / reduction))

        return lmao


def default_time_signature_factory():
    return TimeSignature()