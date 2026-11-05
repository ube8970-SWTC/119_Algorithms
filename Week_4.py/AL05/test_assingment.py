"""Unfinished prompts for sort stability, pipeline contracts, and rule revision."""

from copy import deepcopy
from testing import insertion_sort, build_views
from ticket_data import TICKETS
from search_support import id_key, days_key
from pipeline_support import select_open_tickets


def assignment_checks():
    """Check expected orders, stable ties, shared records, and rebuilt query views."""
    # Sorting: cover the edge cases and several input arrangements. The key is
    # deliberately independent of the ticket schema for the stability fixture.
    assert insertion_sort([], key=lambda item: item[0]) == []
    singleton = [(1, "only")]
    singleton_result = insertion_sort(singleton, key=lambda item: item[0])
    assert singleton_result == singleton
    assert singleton_result is not singleton

    fixture = [(2, "first-2"), (1, "first-1"), (2, "second-2"),
               (3, "only-3"), (1, "second-1")]
    for source in (fixture, sorted(fixture, key=lambda item: item[0]),
                   sorted(fixture, key=lambda item: item[0], reverse=True),
                   [fixture[i] for i in (3, 0, 4, 2, 1)]):
        original = deepcopy(source)
        result = insertion_sort(source, key=lambda item: item[0])
        assert result == sorted(original, key=lambda item: item[0])
        assert source == original
        assert result is not source
    stable = insertion_sort(fixture, key=lambda item: item[0])
    assert [item[1] for item in stable if item[0] == 1] == ["first-1", "second-1"]
    assert [item[1] for item in stable if item[0] == 2] == ["first-2", "second-2"]

    # Ticket sorting must create a new list while retaining the original records.
    seed_snapshot = deepcopy(TICKETS)
    ordered = insertion_sort(TICKETS, key=days_key)
    assert ordered == sorted(TICKETS, key=days_key)
    assert ordered is not TICKETS
    assert len(ordered) == len(TICKETS)
    assert all(any(record is original for original in TICKETS) for record in ordered)
    assert TICKETS == seed_snapshot

    # A small deterministic trace checks counts, order, and equal-key stability.
    small = fixture
    small_sorted = insertion_sort(small, key=lambda item: item[0])
    assert len(small_sorted) == 5
    assert [item[1] for item in small_sorted] == [
        "first-1", "second-1", "first-2", "second-2", "only-3"
    ]

    # Selection is checked at each requested boundary. Returned records must be
    # seed records, and stricter thresholds may only remove earlier selections.
    selected_by_threshold = {
        threshold: select_open_tickets(TICKETS, threshold)
        for threshold in (4, 7, 8)
    }
    for threshold, selected in selected_by_threshold.items():
        expected = [ticket for ticket in TICKETS
                    if any(ticket is chosen for chosen in selected)
                    and days_key(ticket) >= threshold]
        assert len(expected) == len(selected)
        assert all(any(ticket is seed for seed in TICKETS) for ticket in selected)
    assert {id(ticket) for ticket in selected_by_threshold[8]} <= {
        id(ticket) for ticket in selected_by_threshold[7]
    }
    assert {id(ticket) for ticket in selected_by_threshold[7]} <= {
        id(ticket) for ticket in selected_by_threshold[4]
    }

    # Rebuild both query views from the selected records and verify their order.
    for threshold, selected in selected_by_threshold.items():
        display_view, search_view = build_views(selected)
        assert [id_key(ticket) for ticket in display_view] == [
            id_key(ticket) for ticket in sorted(selected, key=days_key)
        ]
        assert [id_key(ticket) for ticket in search_view] == [
            id_key(ticket) for ticket in sorted(selected, key=id_key)
        ]
        assert {id(ticket) for ticket in display_view} == {id(ticket) for ticket in selected}
        assert {id(ticket) for ticket in search_view} == {id(ticket) for ticket in selected}


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run tests without -O so assertions are enabled.")
    assignment_checks()
    print("AL05 checks passed.")