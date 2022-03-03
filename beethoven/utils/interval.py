def is_interval_perfect(interval: int) -> bool:
    within_octave_interval = ((int(interval) - 1) % 7) + 1

    return within_octave_interval in (1, 4, 5)
