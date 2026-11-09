"""Focused checks for AL06 scenarios and interactive selection."""

from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO
from unittest.mock import patch

from main import main, recursive_total, iterative_total
from scenario_data import SCENARIOS, make_entry, make_group


def assignment_checks(scenario):
    """Check scenario totals, boundary/nested cases, invalid data, and preservation."""
    data = scenario["data"]
    expected = scenario["expected_total"]
    original = deepcopy(data)

    # Check each implementation against the independently supplied answer.
    assert recursive_total(data, scenario["included_status"]) == expected
    assert data == original
    assert iterative_total(data, scenario["included_status"]) == expected
    assert data == original

    included = scenario["included_status"]
    excluded = scenario["excluded_status"]

    def check(group, expected_total, included_status):
        before = deepcopy(group)
        assert recursive_total(group, included_status) == expected_total
        assert group == before
        assert iterative_total(group, included_status) == expected_total
        assert group == before

    # Equal amounts with distinct statuses make inclusion/exclusion explicit.
    included_entry = make_entry("Included", 7, included)
    excluded_entry = make_entry("Excluded", 7, excluded)
    no_matches = make_group("No matches", [make_entry("Excluded", 11, excluded)])
    mixed = make_group("Mixed", [
        included_entry,
        excluded_entry,
        make_entry("Zero", 0, included),
        make_group("Nested", [
            make_entry("Included", 5, included),
            make_entry("Excluded", 5, excluded),
        ]),
        make_group("Empty", []),
        no_matches,
    ])

    check(included_entry, 7, included)
    check(excluded_entry, 0, included)
    check(make_entry("Zero", 0, included), 0, included)
    check(make_group("Empty", []), 0, included)
    check(make_group("Flat", [
        make_entry("First", 3, included),
        make_entry("Second", 4, included),
    ]), 7, included)
    check(no_matches, 0, included)
    check(mixed, 12, included)
    check(make_group("Outer", [mixed]), 12, included)

    # Malformed amounts must be rejected even when their status is excluded.
    malformed = make_group(
        "Malformed", [make_entry("Bad amount", "not an amount", excluded)]
    )
    for total_function in (recursive_total, iterative_total):
        try:
            total_function(malformed, included)
        except ValueError:
            pass
        else:
            raise AssertionError(f"{total_function.__name__} accepted malformed data")


def display_checks():
    """Check individual and all-scenario selections."""
    for name, scenario in SCENARIOS.items():
        output = StringIO()
        with patch("builtins.input", return_value=name), redirect_stdout(output):
            main()

        displayed = output.getvalue()
        assert scenario["title"] in displayed
        assert all(
            other["title"] not in displayed
            for other_name, other in SCENARIOS.items()
            if other_name != name
        )

    output = StringIO()
    with patch("builtins.input", return_value="all"), redirect_stdout(output):
        main()
    displayed = output.getvalue()
    assert all(scenario["title"] in displayed for scenario in SCENARIOS.values())

    output = StringIO()
    with patch("builtins.input", side_effect=["unknown", "inventory"]), redirect_stdout(output):
        main()
    assert "Invalid choice." in output.getvalue()
    assert SCENARIOS["inventory"]["title"] in output.getvalue()
    assert SCENARIOS["fundraiser"]["title"] not in output.getvalue()


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Run tests without -O so assertions remain enabled.")
    for scenario in SCENARIOS.values():
        assignment_checks(scenario)
    display_checks()
    print("AL06 checks passed.")