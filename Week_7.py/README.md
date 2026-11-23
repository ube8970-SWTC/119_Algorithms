# AL08: Workshop Access — Traversal and Restricted Routes

Name: [Dylan]
Partner(s): [Garrett]
My contribution: [brief individual/modeling and shared-development notes]
Issued personal case: [A / B / C] wasn't in class so made added an input function to be able to do all of them. 

## Run

```powershell
py -3.14 main.py
py -3.14 test_assignment.py
```

Final settings: STAGE = 3 and TEST_STAGE = 3 if using the starter switches.

## Work Notes

- Model: rooms are nodes and permitted passages are two-way edges; undirected edges capture that both rooms may enter through the passage. Distance, travel time, and capacity are not represented.
- Monday check: the declared Annex has an empty neighbor list and is valid but unreachable because no passage connects it to the main component; the validator checks declared nodes and reciprocal connections.
- Traversal: BFS marks rooms discovered when they are enqueued, while DFS skips rooms that are already visited when they are popped. Visited state prevents cycles from repeating processing.
- Personal restriction: complete this note after the instructor-issued case is known and the Thursday route work is finished.
- Collaboration: we compared model assumptions and route expectations, then shared responsibility for implementing and checking the graph workflow.


## Monday's Model Check

AL08 uses an undirected graph where rooms are nodes and permitted passages are edges bidirectional. The model omits things like distance between rooms. The Annex is valid in the graph structure (a declared empty neighbor list) but unreachable from Entrance because no edge connects it to the main component. Validation ensures all references exist and all edges are reciprocal (undirected property). 

## Tuesday Traversal Workflow

- Used the supplied validation and snapshot helpers; implemented BFS with a queue and discovery-on-enqueue, then iterative DFS with a stack and visited-on-pop.
- Checked both traversals on a small cyclic graph and a disconnected start, then on the workshop graph: each reaches 11 rooms and examines 26 adjacency entries; Annex is unreachable.
- Tests verify visit order, no repeated processing, adjacency counts, and that traversal leaves the input graph unchanged.

## Assistance

Used the supplied validation and snapshot helpers, plus the starter traversal structure and test suite. 

## Instructor Comments

[Reserved for instructor feedback.]