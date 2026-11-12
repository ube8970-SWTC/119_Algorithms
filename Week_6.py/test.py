"""Optional AL07 scaffold: Tuesday payment choices, Thursday saved answers."""

from investigation_support import validate_change
from investigation_display import run

ENABLE_MEMOIZATION = True  # Change to True after Thursday's helper works.


# TUESDAY — Implement the local choice; the reference solver is supplied.
def greedy_change(denominations, target):
    """Return largest-first exact change, or None when that choice gets stuck."""
    coins = validate_change(denominations, target)
    chosen = []
    unpaid = target
    for coin in coins:
        while coin <= unpaid:
            chosen.append(coin)
            unpaid -= coin
    return chosen if unpaid == 0 else None


# THURSDAY — The recurrence and counters are supplied; add lookup and storage.
def calculate_cached(n, cache, counts):
    """Return F(n), reusing saved answers while counting all calls and hits."""
    counts["calls"] += 1
    if n in cache:
        counts["hits"] += 1
        return cache[n]
    if n < 2:
        result = n
    else:
        previous = calculate_cached(n - 1, cache, counts)
        earlier = calculate_cached(n - 2, cache, counts)
        result = previous + earlier
    cache[n] = result
    return result


def main():
    """Present the completed stages using the supplied driver and reports."""
    run(greedy_change, calculate_cached, ENABLE_MEMOIZATION)


if __name__ == "__main__":
    main()