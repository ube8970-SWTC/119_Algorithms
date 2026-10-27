# AL03: Ticket Registry, Queue, and Undo

Name: [your name]
Partners: [name(s)]
Shared repository: [URL]
My contribution: [brief note]

## Run

Keep main.py, testing_1.py, ticket_data.py, ticket_data_testing.py, ticket_display.py,
console_style.py, and any other imported modules together.

```powershell
py -3.14 main.py
py -3.14 test_assignment.py
```

## Operation Comparison

One short reason per row is enough. Compare list and dictionary behavior;
do not implement every operation twice or maintain two live stores.

A list lookup by ID is O(n); a dictionary lookup is O(1) on average.


| Operation | Representation fit / reason |
| --- | --- |
| Find one ticket by ID | A list requires an O(n) scan; a dictionary finds an ID in O(1) average time. |
| Update one ticket's priority | A list must first scan in O(n); a dictionary locates the ticket in O(1) average time, then either can update it. |
| Select tickets in a category | A set would be a list of categories and which Id's are in each category. This makes it so that to see each each in a category you don't have to search the whole database. |

## Work Notes and Reflections

Append brief observations, debugging challenges, changes, and learnings.
found a way to write into a .py file while we were doing the assignment. Could be useful at a later date.


- Processing and undo: [When T302 is undone, it goes to the "waiting work" area. The rest stay the same.]
- Contract or snapshot learning: [Have to make sure every list/dictionary is properly updated for every action]

These can be short bullets, not an essay or separate evidence document.

## Assistance

[Support used, or none. For AI, identify the tool/task and what you checked,
changed, or rejected. Identify the supplied data and display modules as supplied.]

used Ai to add a repair queue function. it would take any updates from ticket_data.py and input them into the queue

## Instructor Comments

[Reserved for instructor feedback.]