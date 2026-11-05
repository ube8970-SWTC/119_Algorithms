"""Unfinished prompts for sort stability, pipeline contracts, and rule revision."""

from copy import deepcopy
from testing import insertion_sort, build_views
from ticket_data import TICKETS
from search_support import id_key, days_key
from pipeline_support import select_open_tickets


def assignment_checks():
    """Check expected orders, stable ties, shared records, and rebuilt query views."""
    empty_result, comparisons, moves, trace = insertion_sort(
        [], key=lambda item: item["rank"]
    )
    assert empty_result == []
    assert (comparisons, moves, trace) == (0, 0, [])

    singleton = [(1, "only")]
    singleton_result, comparisons, moves, trace = insertion_sort(
        singleton, key=lambda item: item[0]
    )
    assert singleton_result == singleton, (
        "insertion_sort must return the singleton input's contents"
    )
    assert singleton_result is not singleton, (
        "insertion_sort must return a new list, not the input list"
    )
    assert (comparisons, moves, trace) == (0, 0, [])

    fixture = [
        {"id": "T2A", "rank": 2, "label": "first-2"},
        {"id": "T1A", "rank": 1, "label": "first-1"},
        {"id": "T2B", "rank": 2, "label": "second-2"},
        {"id": "T3", "rank": 3, "label": "only-3"},
        {"id": "T1B", "rank": 1, "label": "second-1"},
    ]
    for source in (fixture, sorted(fixture, key=lambda item: item["rank"]),
                   sorted(fixture, key=lambda item: item["rank"], reverse=True),
                   [fixture[i] for i in (3, 0, 4, 2, 1)]):
        original = deepcopy(source)
        result, _, _, _ = insertion_sort(source, key=lambda item: item["rank"])
        assert result == sorted(original, key=lambda item: item["rank"])
        assert source == original
        assert result is not source
    stable = insertion_sort(fixture, key=lambda item: item["rank"])[0]
    assert [item["label"] for item in stable if item["rank"] == 1] == [
        "first-1", "second-1"
    ]
    assert [item["label"] for item in stable if item["rank"] == 2] == [
        "first-2", "second-2"
    ]

    # Ticket sorting must create a new list while retaining the original records.
    seed_snapshot = deepcopy(TICKETS)
    ordered, _, _, _ = insertion_sort(TICKETS, key=days_key)
    assert ordered == sorted(TICKETS, key=days_key)
    assert ordered is not TICKETS
    assert len(ordered) == len(TICKETS)
    assert all(
        result is expected
        for result, expected in zip(ordered, sorted(TICKETS, key=days_key))
    )
    assert TICKETS == seed_snapshot

    # A small deterministic trace checks counts, order, and equal-key stability.
    small_sorted, comparisons, moves, trace = insertion_sort(
        fixture, key=lambda item: item["rank"]
    )
    assert len(small_sorted) == 5
    assert [item["label"] for item in small_sorted] == [
        "first-1", "second-1", "first-2", "second-2", "only-3"
    ]
    assert (comparisons, moves) == (7, 4)
    assert trace == [
        ["T1A", "T2A", "T2B", "T3", "T1B"],
        ["T1A", "T2A", "T2B", "T3", "T1B"],
        ["T1A", "T2A", "T2B", "T3", "T1B"],
        ["T1A", "T1B", "T2A", "T2B", "T3"],
    ]

    # Selection is checked at each requested boundary. Returned records must be
    # seed records, and stricter thresholds may only remove earlier selections.
    expected_ids = {
        4: ["T403", "T405", "T402", "T406"],
        7: ["T403", "T405"],
        8: [],
    }
    selected_by_threshold = {
        threshold: select_open_tickets(TICKETS, threshold)
        for threshold in (4, 7, 8)
    }
    for threshold, selected in selected_by_threshold.items():
        assert [id_key(ticket) for ticket in selected] == expected_ids[threshold]
        assert all(any(ticket is seed for seed in TICKETS) for ticket in selected)
        assert selected is not TICKETS
    assert {id(ticket) for ticket in selected_by_threshold[8]} <= {
        id(ticket) for ticket in selected_by_threshold[7]
    }
    assert {id(ticket) for ticket in selected_by_threshold[7]} <= {
        id(ticket) for ticket in selected_by_threshold[4]
    }

    # Rebuild both query views from the selected records and verify their order.
    for threshold, selected in selected_by_threshold.items():
        rebuilt_selected, display_view, search_view = build_views(
            TICKETS, minimum_days=threshold
        )
        assert [id_key(ticket) for ticket in rebuilt_selected] == expected_ids[
            threshold
        ]
        assert rebuilt_selected is not selected
        assert [id_key(ticket) for ticket in display_view] == [
            id_key(ticket) for ticket in sorted(selected, key=days_key)
        ], f"display_view is not ordered by days_key (threshold {threshold})"
        assert [id_key(ticket) for ticket in search_view] == [
            id_key(ticket) for ticket in sorted(selected, key=id_key)
        ], f"search_view is not ordered by id_key (threshold {threshold})"
        assert {
            id(ticket) for ticket in display_view
        } == {id(ticket) for ticket in selected}, (
            f"display_view must retain the selected ticket records (threshold {threshold})"
        )
        assert {
            id(ticket) for ticket in search_view
        } == {id(ticket) for ticket in selected}, (
            f"search_view must retain the selected ticket records (threshold {threshold})"
        )
        assert all(
            result is expected
            for result, expected in zip(display_view, sorted(selected, key=days_key))
        )
        assert all(
            result is expected
            for result, expected in zip(search_view, sorted(selected, key=id_key))
        )
    assert TICKETS == seed_snapshot


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run tests without -O so assertions are enabled.")
    assignment_checks()
    print("AL05 checks passed.")