# AL05: Filter, Sort, and Search Pipeline

Name: [Dylan Ubersox]
My contribution: [I wrote the assignment; individual assignment]

## Run

Keep task_1.py, test_assignment.py, search_algorithms.py, ticket_data.py,
search_support.py, pipeline_support.py, ticket_display.py, and console_style.py together.

```powershell
py -3.14 task_1.py
py -3.14 test_assignment.py
```

## Pipeline and Work Notes

- Pipeline: `ticket_data.py` supplies the tickets; the pipeline filters them by the requested day window, prepares display and search views, and looks up a ticket.
- One request: A direct scan avoids the setup cost of building a reusable search view for a single lookup.
- Repeated requests: Reuse the prepared view for lookups; rebuild it when the source data or filter window changes, accounting for its storage cost.
- Issued change: The filter window changed from 4 to 7 days; the search algorithms themselves stayed the same.
- Copying/stability or debugging learning: Filtering a copy preserves the original ticket data; check the filter boundary when changing the window.

Short bullets are enough; traces/counts can stay in the console.

## Assistance

[Identify supplied modules/starter and whether search_algorithms.py is your AL04
work or the instructor-released recovery copy. Identify other help, or none.
I didn't use AL04, started it from provided materials
For AI: tool/task and what you checked, changed, or rejected.]

## Instructor Comments

[Reserved for instructor feedback.]