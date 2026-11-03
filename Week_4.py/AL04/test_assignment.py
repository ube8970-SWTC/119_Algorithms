"""Unfinished test prompts; replace the final stop with your own focused checks."""

from copy import deepcopy
from AL04.Task_1 import linear_search, binary_search
from AL04.ticket_data import TICKETS
from AL04.search_support import id_key, category_key


def assignment_checks():
    """Check independent expected answers, boundaries, traces, and input preservation."""
    def contains(trace, expected):
        if trace == expected:
            return True
        if isinstance(trace, dict):
            return any(contains(value, expected) for value in trace.values())
        if isinstance(trace, (list, tuple, set)):
            return any(contains(value, expected) for value in trace)
        return False

    def missing(result):
        assert result is None or result == -1

    fixture_before = deepcopy(TICKETS)
    tickets = deepcopy(TICKETS)
    assert tickets

    # Derive the answer independently from the fixture, not from another search.
    first_id = id_key(tickets[0])
    expected_first = next(i for i, ticket in enumerate(tickets)
                          if id_key(ticket) == first_id)
    trace = []
    assert linear_search(tickets, first_id, key=id_key, trace=trace) == expected_first
    assert contains(trace, tickets[expected_first]) or contains(trace, first_id)
    last_id = id_key(tickets[-1])
    expected_last = next(i for i, ticket in enumerate(tickets)
                         if id_key(ticket) == last_id)
    assert linear_search(tickets, last_id, key=id_key) == expected_last
    missing(linear_search(tickets, "", key=id_key))
    missing(linear_search([], first_id, key=id_key))
    singleton = [deepcopy(tickets[0])]
    assert linear_search(singleton, first_id, key=id_key) == 0
    missing(linear_search(singleton, "", key=id_key))

    by_id = sorted(deepcopy(tickets), key=id_key)
    ids = [id_key(ticket) for ticket in by_id]
    assert ids == sorted(ids) and len(ids) >= 2
    below, above = "", "\U0010ffff"
    between = ids[0] + "\0"
    assert below not in ids and above not in ids
    assert ids[0] < between < ids[1] and between not in ids
    for target in (ids[0], ids[-1]):
        expected = next(i for i, ticket in enumerate(by_id) if id_key(ticket) == target)
        trace = []
        assert binary_search(by_id, target, key=id_key, trace=trace) == expected
        assert contains(trace, by_id[expected]) or contains(trace, target)
    for target in (below, between, above):
        trace = []
        missing(binary_search(by_id, target, key=id_key, trace=trace))

    # Duplicate categories are valid: verify the returned item's category.
    by_category = sorted(deepcopy(tickets), key=category_key)
    categories = [category_key(ticket) for ticket in by_category]
    wanted_category = categories[len(categories) // 2]
    trace = []
    position = binary_search(by_category, wanted_category, key=category_key, trace=trace)
    assert isinstance(position, int) and 0 <= position < len(by_category)
    assert category_key(by_category[position]) == wanted_category
    assert contains(trace, by_category[position]) or contains(trace, wanted_category)
    missing(binary_search(by_category, "\U0010ffff", key=category_key))

    # T401 is deliberately searched in the fixture's unsorted ID order.
    missing(binary_search(TICKETS, "T401", key=id_key))
    assert TICKETS == fixture_before
    assert tickets == fixture_before


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run tests without -O so assertions are enabled.")
    assignment_checks()
    print("AL04 checks passed.")