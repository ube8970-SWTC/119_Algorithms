"""Optional focused check starting points; expand them across the week."""

from network_support import validate_model
from main import breadth_first, depth_first, shortest_hop_path, MY_RESTRICTION

TEST_STAGE = 1  # Raise to 2 Tuesday and 3 Thursday after completing those tests.


def test_model():
    """Begin Monday with a clearly valid two-way model and an unknown reference."""
    assert validate_model({"A": ["B"], "B": ["A"]}) == []
    assert validate_model({"A": ["Missing"]})
    broken = {"A": ["B"], "B": []}
    assert validate_model(broken)
    repaired = {"A": ["B"], "B": ["A"]}
    assert validate_model(repaired) == []


def test_traversals():
    """Check independent expectations before trying the full workshop fixture."""
    tiny = {"A": ["B", "C"], "B": ["A"], "C": ["A"], "D": []}
    original = {room: neighbors.copy() for room, neighbors in tiny.items()}

    breadth_order = breadth_first(tiny, "A")
    depth_order = depth_first(tiny, "A")
    assert breadth_order == ["A", "B", "C"]
    for order in (breadth_order, depth_order):
        assert order[0] == "A"
        assert set(order) == {"A", "B", "C"}
        assert len(order) == len(set(order))
        assert len(tiny) == 4
        assert tiny == original


def test_paths_and_personal_case():
    """Check route boundaries and your issued blocked-node result independently."""
    model = {
        "A": ["B", "C"],
        "B": ["A", "D"],
        "C": ["A", "D"],
        "D": ["B", "C"],
        "E": [],
    }
    original = {room: neighbors.copy() for room, neighbors in model.items()}

    path = shortest_hop_path(model, "A", "D")
    assert path == ["A", "B", "D"]
    assert len(path) - 1 == 2
    assert path[0] == "A" and path[-1] == "D"
    assert all(right in model[left] for left, right in zip(path, path[1:]))
    assert shortest_hop_path(model, "A", "A") == ["A"]
    assert shortest_hop_path(model, "A", "E") is None
    assert shortest_hop_path(model, "A", "D", "A") is None

    personal = {
        "Start": [MY_RESTRICTION, "Detour"],
        MY_RESTRICTION: ["Start", "Goal"],
        "Detour": ["Start", "Goal"],
        "Goal": [MY_RESTRICTION, "Detour"],
    }
    personal_original = {
        room: neighbors.copy() for room, neighbors in personal.items()
    }
    personal_path = shortest_hop_path(
        personal, "Start", "Goal", MY_RESTRICTION
    )
    assert personal_path == ["Start", "Detour", "Goal"]
    assert personal_path[0] == "Start" and personal_path[-1] == "Goal"
    assert len(personal_path) - 1 == 2
    assert MY_RESTRICTION not in personal_path
    assert all(
        right in personal[left]
        for left, right in zip(personal_path, personal_path[1:])
    )
    assert model == original
    assert personal == personal_original


if __name__ == "__main__":
    test_model()
    if TEST_STAGE >= 2:
        test_traversals()
    if TEST_STAGE >= 3:
        test_paths_and_personal_case()
    print("Selected-stage starting checks passed; complete all stages before submission.")