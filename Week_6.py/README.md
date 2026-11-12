# Algorithms_paired_Dylan_Ty
# AL07: Greedy Claims and Memoization Evidence

Name: [Dylan]
Partner(s): [Ty]
My contribution: [brief note, including role changes]

## Run

```powershell
py -3.14 main.py
py -3.14 main.py --n 5
py -3.14 test_assignment.py
```

The --n option is used after enabling Thursday's stage.

## Work Notes

- Payment finding: With coins 1, 3, and 4, greedy makes 6 as 4+1+1, while 3+3 uses fewer coins; this disproves that greedy is always optimal.
- Saved-answer finding: For fib(6), plain recursion makes 25 calls; memoization computes each of the 7 values once, trading O(n) storage for fewer calls.
- Pair question/decision: Should a zero target need any coins? We decided the base case returns 0, so exact combinations can build on it.

Keep observations brief. Append debugging/learnings as useful; no separate report.
Shared code/results are allowed; these observations are in your own words.

## Assistance

[Identify supplied files and other help. For AI, name the task/tool and what you
checked, changed, or rejected. No AI use is required.]
Used AI to try to fix a host of issues with VS code not having the explorer extension on the left of the screen. 
## Instructor Comments

[Reserved for instructor feedback.]