---
description: Compare options (libraries, APIs, services) with live sources and get one recommendation. Usage: /research <question>
argument-hint: <question>
---

Research: $ARGUMENTS

1. If `$ARGUMENTS` is empty, ask what decision needs researching and wait.
2. Run the `build-crew:researcher` subagent with the question and any constraints the user gave.
3. Reply in ≤ 6 lines: the recommendation, the runner-up and when to pick it, and 2–3 source links.
4. If `docs/HOW_IT_WORKS.md` exists, ask: "Add this to Decisions?" On a yes, paste the `DECISION_ROW` into the Decisions table.
