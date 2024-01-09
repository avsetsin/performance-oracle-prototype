def to_eth(value: int) -> float:
    return value / 10**9


def format_gwei(value: int) -> str:
    return format(to_eth(value), ".5f") + " eth"
