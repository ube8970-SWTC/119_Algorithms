"""Optional English-first starter for stable sorting and a key-correct pipeline."""

from ticket_data import TICKETS
from search_support import id_key, days_key
from pipeline_support import select_open_tickets
from ticket_display import show_ticket, show_tickets

# After preparing your local search_algorithms.py, add its search imports here.
# Copy your AL04 functions/imports, or use the instructor-released recovery module.


# TUESDAY - Stable ordering, with counts for one tiny example.

def insertion_sort(records, key):
    """Return a stable shallow ordered list, comparison/shift counts, and ID trace."""
    ordered = list(records)
    comparisons = 0
    shifts = 0
    trace = []

    for index in range(1, len(ordered)):
        item = ordered[index]
        item_key = key(item)
        position = index - 1

        while position >= 0:
            comparisons += 1
            if not item_key < key(ordered[position]):
                break
            ordered[position + 1] = ordered[position]
            shifts += 1
            position -= 1

        ordered[position + 1] = item
        trace.append([id_key(record) for record in ordered])

    return ordered, comparisons, shifts, trace


# THURSDAY - Compose existing interfaces; rebuild after the eligibility change.

def build_views(records, minimum_days=4):
    """Return selected, age-display, and ID-search lists sharing eligible records."""
    selected = select_open_tickets(records, minimum_days)
    age_display, _, _, _ = insertion_sort(selected, days_key)
    id_search = sorted(selected, key=id_key)
    return selected, age_display, id_search


def main():
    """Present completed daily stages and explain the issued threshold change."""
    original_ids = [id_key(ticket) for ticket in TICKETS]
    selected, age_display, id_search = build_views(TICKETS, minimum_days=4)

    # Verify both ordering and stability without changing the source records.
    checked, comparisons, shifts, trace = insertion_sort(selected, days_key)
    assert checked == sorted(selected, key=days_key)
    assert [id_key(ticket) for ticket in TICKETS] == original_ids
    assert all(
        checked_ticket is selected_ticket
        for checked_ticket, selected_ticket in zip(
            sorted(selected, key=days_key), checked
        )
    )

    print("Open tickets aged at least 4 days, stable age order:")
    print(" ".join(str(id_key(ticket)) for ticket in age_display))
    print("ID search order:")
    print(" ".join(str(id_key(ticket)) for ticket in id_search))

    tiny_sorted, tiny_comparisons, tiny_shifts, trace = insertion_sort(
        selected[:5], days_key
    )
    print("Tiny example ID trace:", trace)
    print(f"Tiny example comparisons: {tiny_comparisons}; right-shifts: {tiny_shifts}")

    for threshold in (7, 8):
        revised, revised_age, _ = build_views(TICKETS, minimum_days=threshold)
        ids = " ".join(str(id_key(ticket)) for ticket in revised_age)
        print(f"Minimum age {threshold}: {len(revised)} ticket(s) {ids}")


if __name__ == "__main__":
    main()