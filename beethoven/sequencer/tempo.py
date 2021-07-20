from dataclasses import dataclass


@dataclass(order=True)
class Tempo:
    bpm: int = 120

    def base_time_unit(self) -> float:
        """Compute the time duration in second of a single measure."""
        return 60 / self.bpm
