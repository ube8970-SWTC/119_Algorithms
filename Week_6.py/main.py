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

def main():
    """Present the completed stages using the supplied driver and reports."""
    run(greedy_change, None, ENABLE_MEMOIZATION)

if __name__ == "__main__":
    main()