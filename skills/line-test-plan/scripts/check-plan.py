#!/usr/bin/env python3
"""Check that a PLAN.md follows the line-test-plan contract.

Usage: python3 check-plan.py test/<feature-slug>/PLAN.md

Checks: a `## Test data` section with at least one bullet; lettered sections
(`## A. Title`); tables with the columns #, Platform, Phase, Action, Checks,
Evidence, Result; step IDs matching ^[A-Z][0-9]+$ and unique; Phase one of
before | capture | after; a `## Run order` section.
Exits 1 and lists every problem when the plan does not conform.
"""

import re
import sys

COLUMNS = ["#", "Platform", "Phase", "Action", "Checks", "Evidence", "Result"]
PHASES = ["before", "capture", "after"]
STEP = re.compile(r"^[A-Z][0-9]+$")


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def main(path):
    problems = []
    text = open(path, encoding="utf-8").read().splitlines()

    sections = [i for i, l in enumerate(text) if re.match(r"^## [A-Z]\. ", l)]
    if not sections:
        problems.append("no lettered sections (## A. Title)")
    in_test_data, bullets = False, 0
    for l in text:
        if l.startswith("## "):
            in_test_data = l.strip() == "## Test data"
        elif in_test_data and l.lstrip().startswith(("- ", "* ")):
            bullets += 1
    if not any(l.strip() == "## Test data" for l in text):
        problems.append("missing `## Test data` section")
    elif not bullets:
        problems.append("`## Test data` has no bullets (list every dummy string, or `- none`)")

    seen, phase_log = set(), []
    header = None
    for n, l in enumerate(text, 1):
        if re.match(r"^## ", l):
            header = None
        if not l.lstrip().startswith("|"):
            header = None if not l.strip() else header
            continue
        c = cells(l)
        if c and c[0] == "#":
            header = c
            if c != COLUMNS:
                problems.append(f"line {n}: columns are {c}, expected {COLUMNS}")
            continue
        if set("".join(c)) <= set("-: "):
            continue
        if header != COLUMNS or len(c) != len(COLUMNS):
            if header is not None:
                problems.append(f"line {n}: row has {len(c)} cells, expected {len(COLUMNS)}")
            continue
        sid, platform, phase = c[0], c[1], c[2]
        if not STEP.match(sid):
            problems.append(f"line {n}: step ID {sid!r} does not match ^[A-Z][0-9]+$")
        elif sid in seen:
            problems.append(f"line {n}: duplicate step ID {sid}")
        seen.add(sid)
        if phase not in PHASES:
            problems.append(f"line {n}: {sid} phase {phase!r} is not one of {PHASES}")
        else:
            phase_log.append((sid, phase))
        if not platform:
            problems.append(f"line {n}: {sid} has no platform")

    if not seen:
        problems.append("no step rows found")

    order = re.search(r"^## Run order\s*$", "\n".join(text), re.M)
    if not order:
        problems.append("missing `## Run order` section (before, then capture, then after)")

    if problems:
        print(f"{path}: {len(problems)} problem(s)")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print(f"{path}: ok, {len(seen)} steps")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
