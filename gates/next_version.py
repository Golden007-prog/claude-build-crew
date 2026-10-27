#!/usr/bin/env python3
"""next_version — compute the next SemVer from Conventional Commits. Code, not AI.

Usage: next_version.py [ref]   (default: origin/HEAD, falls back to HEAD)

Rules (since the last v* tag):
  BREAKING CHANGE or `type!:` -> major (minor while on 0.x; going to 1.0.0 is a human decision,
                                 pass it to /release explicitly)
  feat                        -> minor
  fix / perf                  -> patch
  nothing user-facing         -> exit 1, nothing to release
"""
from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import emit, git, main_guarded  # noqa: E402

SEP = "\x1e"


def parse(v: str) -> tuple[int, int, int]:
    m = re.match(r"v?(\d+)\.(\d+)\.(\d+)", v)
    return tuple(int(x) for x in m.groups()) if m else (0, 0, 0)


def main() -> None:
    ref = sys.argv[1] if len(sys.argv) > 1 else (git("symbolic-ref", "--short", "refs/remotes/origin/HEAD") or "HEAD")
    # releases only: pre-release tags (v1.0.0-rc.1) are not a base for the next version
    last = git("describe", "--tags", "--abbrev=0", "--match", "v[0-9]*", "--exclude", "*-*", ref)
    rng = f"{last}..{ref}" if last else ref
    log = git("log", rng, f"--pretty=format:%H%n%s%n%b{SEP}")
    commits = [c.strip() for c in log.split(SEP) if c.strip()]

    bump, why = None, None
    rank = {"patch": 1, "minor": 2, "major": 3}
    for c in commits:
        sha, _, rest = c.partition("\n")
        subject = rest.split("\n", 1)[0]
        kind = None
        if "BREAKING CHANGE" in rest or re.match(r"^\w+(\(.+\))?!:", subject):
            kind = "major"
        elif re.match(r"^feat(\(.+\))?:", subject):
            kind = "minor"
        elif re.match(r"^(fix|perf)(\(.+\))?:", subject):
            kind = "patch"
        if kind and (bump is None or rank[kind] > rank[bump]):
            bump, why = kind, f"{sha[:7]} {subject}"

    cur = parse(last) if last else (0, 0, 0)
    out = {"gate": "next_version", "last_tag": last or None, "commits": len(commits)}
    if not bump:
        out["note"] = "nothing user-facing to release (only docs/chore/test/refactor/ci)"
        emit(out, False)
    if bump == "major" and cur[0] == 0:
        bump = "minor"
    major, minor, patch = cur
    nxt = {"major": (major + 1, 0, 0), "minor": (major, minor + 1, 0), "patch": (major, minor, patch + 1)}[bump]
    if not last and nxt == (0, 0, 1):
        nxt = (0, 1, 0)
    out.update(current="%d.%d.%d" % cur, next="%d.%d.%d" % nxt, bump=bump, decided_by=why)
    emit(out, True)


if __name__ == "__main__":
    main_guarded("next_version", main)
