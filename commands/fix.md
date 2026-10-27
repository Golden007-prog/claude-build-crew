---
description: Fix a bug — reproduce, root-cause, regression test, minimal fix — then hand off to /ship. Usage: /fix <bug, error, or #issue>
argument-hint: <bug description or #issue>
---

Fix: $ARGUMENTS

1. If `$ARGUMENTS` is empty, ask for expected vs actual behavior and the error text, then wait. For `#123` or an issue URL, run `gh issue view <n> --json title,body,comments`.
2. `git status --porcelain` must be empty. If not, STOP with "Commit or stash first."
3. `git switch <default> && git pull --ff-only && git switch -c fix/<kebab-summary>`.
4. Run the `build-crew:debugger` subagent with the full report. If it returns STOPPED, show what it tried and what it needs, then END.
5. If the fix changed user-visible behavior described in `docs/HOW_IT_WORKS.md`, update that line. Otherwise leave it alone.
6. Report the root cause, files changed, the regression test, and the checks result. Mention `Fixes #<n>` if the bug came from an issue. Then: "Run `/ship`."
