"""Optional focused check starting points; expand them across the week."""

from copy import deepcopy

from network_support import validate_model
from main import breadth_first, depth_first, shortest_hop_path, MY_RESTRICTION

TEST_STAGE = 3  # Raise to 3 Thursday after completing the route tests.


def test_model():
    """Begin Monday with a clearly valid two-way model and an unknown reference."""
    assert validate_model({"A": ["B"], "B": ["A"]}) == []
    assert validate_model({"A": ["Missing"]})
    # Add your one broken-and-repaired copy of the workshop model.


def test_traversals():
    """Check independent expectations before trying the full workshop fixture."""
    tiny = {"A": ["B", "C"], "B": ["A"], "C": ["A"], "D": []}
    original = deepcopy(tiny)

    bfs_order, _, bfs_edges = breadth_first(tiny, "A")
    # Expected BFS order
    assert bfs_order == ["A", "B", "C"]
    # No repeated BFS processing
    assert len(bfs_order) == len(set(bfs_order))
    # Four BFS adjacency entries
    assert bfs_edges == 4
    # BFS preserves the source graph
    assert tiny == original

    dfs_order, _, dfs_edges = depth_first(tiny, "A")
    # Expected DFS order
    assert dfs_order == ["A", "B", "C"]
    # No repeated DFS processing
    assert len(dfs_order) == len(set(dfs_order))
    # Four DFS adjacency entries
    assert dfs_edges == 4
    # DFS preserves the source graph
    assert tiny == original


def test_paths_and_personal_case():
    """Check route boundaries and your issued blocked-node result independently."""
    from network_data import GRAPH, START, GOAL, RESTRICTIONS
    original = {room: neighbors.copy() for room, neighbors in GRAPH.items()}

    # Check a small known path, start=goal, disconnected goal, and a blocked endpoint.
    path, _ = shortest_hop_path(GRAPH, START, GOAL)
    assert path == ["Entrance", "Reception", "Office", "Loading"]
    assert path[0] == START and path[-1] == GOAL
    assert all(right in GRAPH[left] for left, right in zip(path, path[1:]))

    path_same, _ = shortest_hop_path(GRAPH, START, START)
    assert path_same == ["Entrance"]

    path_annex, _ = shortest_hop_path(GRAPH, START, "Annex")
    assert path_annex is None

    # Import the supplied workshop data and use MY_RESTRICTION for your personal case.
    blocked = RESTRICTIONS[MY_RESTRICTION]["blocked"]
    path_restricted, _ = shortest_hop_path(GRAPH, START, GOAL, blocked)

    # Check exact expected endpoints/hops or None, consecutive connections, no blocked
    # rooms in a returned route, and unchanged source data.
    if path_restricted is not None:
        assert path_restricted[0] == START and path_restricted[-1] == GOAL
        assert all(right in GRAPH[left] for left, right in zip(path_restricted, path_restricted[1:]))
        for blocked_node in blocked:
            assert blocked_node not in path_restricted

    assert GRAPH == original


if __name__ == "__main__":
    test_model()
    if TEST_STAGE >= 2:
        test_traversals()
    if TEST_STAGE >= 3:
        test_paths_and_personal_case()
    print("Selected-stage starting checks passed; complete all stages before submission.")