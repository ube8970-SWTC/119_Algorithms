# AL04: Search Contracts and Correctness

Name: [Dylan]
My contribution: [I wrote the entire assignment]

## Run

Keep Task_1.py, testing.py, test_assignment.py, ticket_data.py, search_support.py,
ticket_display.py, and console_style.py together.

```powershell
py -3.14 Task_1.py
py -3.14 test_assignment.py
```

## Contract and Work Notes

- Ordering precondition: Binary search only works when the searched data is ordered by the same key used for comparison. The original T401 list was not ordered by that key, so narrowing the search range could skip a matching ticket; sorting a copy first satisfies the precondition.
- Result agreement: Searching the original list and a sorted or filtered copy can return different positions because each position refers to its own list. Compare the ticket/category found rather than expecting the indices to match. If a category occurs more than once, either matching occurrence is valid unless the contract specifies which one to return.
- Reflection/debugging/learning: I learned to check a search algorithm's ordering preconditions before debugging its comparisons, and to distinguish a record's identity from its position in a particular list.

The two small traces can stay in console output. No separate report or essay.

## Assistance

[Supplied modules/starter and other help used, or none beyond supplied files.
For AI: tool/task and what you checked, changed, or rejected.]

## Instructor Comments

[Reserved for instructor feedback.]