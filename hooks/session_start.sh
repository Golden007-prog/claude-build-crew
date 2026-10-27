#!/usr/bin/env bash
# SessionStart hook: every new session starts with where things stand.
# Output is added to Claude's context. Silent in projects without build-crew docs.
set -u
DIR="${CLAUDE_PROJECT_DIR:-$PWD}"

if [ -f "$DIR/docs/PROGRESS.md" ]; then
  echo "=== build-crew: last handoff (docs/PROGRESS.md) ==="
  sed -n '1,/^## History/p' "$DIR/docs/PROGRESS.md" | head -60
fi

if [ -f "$DIR/docs/PLAN.md" ]; then
  echo "=== build-crew: phases (docs/PLAN.md) ==="
  grep -E '^- \[( |x)\] Phase' "$DIR/docs/PLAN.md" | head -40
fi

if [ -f "$DIR/docs/HOW_IT_WORKS.md" ]; then
  echo "=== build-crew: docs/HOW_IT_WORKS.md holds the decisions and non-goals. The code is the source of truth for everything else. ==="
fi
exit 0
