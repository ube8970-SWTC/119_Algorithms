"""Optional generic English-first scaffold for any one AL06 application."""

from scenario_data import SCENARIOS
from record_support import validate_node
from record_display import show_records, show_results

# MONDAY — Decide what contributes, then follow the nested structure.

def recursive_total(node, included_status):
    """Return the selected entry amount or recursively combine a group's totals."""
    validate_node(node)
    if node["type"] == "entry":
        return node["amount"] if node["status"] == included_status else 0

    subtotal = 0
    for child in node["items"]:
        subtotal += recursive_total(child, included_status)
    return subtotal


def iterative_total(node, included_status):
    """Total matching entries using an explicit stack without changing the source."""
    pending = [node]
    total = 0
    while pending:
        current = pending.pop()
        validate_node(current)
        if current["type"] == "group":
            pending.extend(current["items"])
        elif current["status"] == included_status:
            total += current["amount"]
    return total


def main():
    """Display one chosen scenario or every available scenario."""
    while True:
        choice = input(
            "Choose a scenario (fundraiser, project, inventory, or all): "
        ).strip().lower()
        if choice == "all":
            scenarios = SCENARIOS.values()
            break
        if choice in SCENARIOS:
            scenarios = (SCENARIOS[choice],)
            break
        print("Invalid choice. Enter fundraiser, project, inventory, or all.")

    for scenario in scenarios:
        recursive_result = recursive_total(
            scenario["data"], scenario["included_status"]
        )
        iterative_result = iterative_total(
            scenario["data"], scenario["included_status"]
        )

        show_records(scenario["data"], scenario["unit"])
        show_results(scenario, recursive_result, iterative_result)


if __name__ == "__main__":
    main()