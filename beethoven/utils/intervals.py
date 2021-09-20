def is_perfect_interval_class(interval: str) -> bool:
    """
    Check if interval correspond to a perfect class interval,
    like unison, fifth, fourth, and theirs octaves
    """
    normalized_interval = ((int(interval) - 1) % 7) + 1

    return normalized_interval in (1, 4, 5)
