#!/usr/bin/env python3
"""Keep test/<feature>/evidence/manifest.json: which screenshot proves which step.

Usage:
  manifest.py --feature test/<slug> pick --step B5 [--platform P] [--phase before|capture|after] [--note T] RAW...
  manifest.py --feature test/<slug> unpick RAW...
  manifest.py --feature test/<slug> set --in-pr yes|no TARGET...    # TARGET: step ID, raw or redacted file
  manifest.py --feature test/<slug> show

--platform and --phase default to the step's row in PLAN.md. Shape:

  {"feature": "<slug>", "updated": "<iso>",
   "steps": {"B5": [{"raw": "raw/<file>", "platform": "LINE iOS", "phase": "after",
                     "redacted": "redacted/B5-line-ios-after.png" | null,
                     "approved": false, "in_pr": true, "note": ""}]}}

"redacted" and "approved" are set by `redact.py final` only. line-pr uploads
only entries with approved true, a redacted file, and in_pr true.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from evidence_lib import PHASES, STEP, Feature, die, load_json, now_iso, parse_plan, save_json, slug  # noqa: E402


def load(feat):
    m = load_json(feat.manifest, None) or {"feature": feat.slug, "steps": {}}
    m.setdefault("steps", {})
    return m


def save(feat, m):
    m["feature"] = feat.slug
    m["updated"] = now_iso()
    m["steps"] = {k: m["steps"][k] for k in sorted(m["steps"], key=lambda s: (s[0], int(s[1:])))}
    save_json(feat.manifest, m)


def entries(m):
    for step, files in m["steps"].items():
        for e in files:
            yield step, e


def find(m, rel_raw):
    for step, e in entries(m):
        if e["raw"] == rel_raw:
            return step, e
    return None, None


def output_name(m, step, entry):
    """<step>-<platform>-<phase>.png, with -2, -3... when another entry already has the name."""
    base = f"{step}-{slug(entry['platform'])}-{entry['phase']}"
    taken = {e.get("redacted") for _, e in entries(m) if e is not entry}
    name, n = f"redacted/{base}.png", 1
    while name in taken:
        n += 1
        name = f"redacted/{base}-{n}.png"
    return name


def cmd_pick(feat, m, a):
    if not STEP.match(a.step):
        die(f"step ID {a.step!r} does not match ^[A-Z][0-9]+$")
    _, steps, _ = parse_plan(feat.plan)
    row = steps.get(a.step, {})
    platform = a.platform or row.get("platform")
    phase = a.phase or row.get("phase")
    if not platform or not phase:
        die(f"{a.step} is not in {feat.plan}; pass --platform and --phase")
    if phase not in PHASES:
        die(f"phase {phase!r} is not one of {PHASES}")
    for r in a.raw:
        rel = feat.rel(feat.raw_image(r))
        old_step, old = find(m, rel)
        if old:
            m["steps"][old_step].remove(old)
            if not m["steps"][old_step]:
                del m["steps"][old_step]
        m["steps"].setdefault(a.step, []).append({
            "raw": rel, "platform": platform, "phase": phase, "redacted": None,
            "approved": False, "in_pr": True, "note": a.note or ""})
        print(f"{a.step} {phase} {platform}: {rel}")


def cmd_unpick(feat, m, a):
    for r in a.raw:
        rel = feat.rel(feat.raw_image(r))
        step, e = find(m, rel)
        if not e:
            print(f"not picked: {rel}")
            continue
        m["steps"][step].remove(e)
        if not m["steps"][step]:
            del m["steps"][step]
        print(f"unpicked {step}: {rel}")


def cmd_set(feat, m, a):
    flag = a.in_pr == "yes"
    for t in a.targets:
        hits = [e for s, e in entries(m) if t in (s, e["raw"], e.get("redacted"), os.path.basename(e["raw"]))]
        if not hits:
            die(f"nothing in the manifest matches {t!r}")
        for e in hits:
            e["in_pr"] = flag
            print(f"in_pr={flag}: {e['raw']}")


def cmd_show(feat, m, a):
    for step, e in entries(m):
        state = "approved" if e.get("approved") else "not approved"
        pr = "in PR" if e.get("in_pr") else "not in PR"
        print(f"{step:5} {e['phase']:8} {e['platform']:20} {e.get('redacted') or '-':40} {state}, {pr}  ({e['raw']})")
        if e.get("redacted") and not os.path.exists(os.path.join(feat.evidence, e["redacted"])):
            print(f"      warning: {e['redacted']} is missing")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--feature", required=True)
    ap.add_argument("--plan")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pick")
    p.add_argument("--step", required=True)
    p.add_argument("--platform")
    p.add_argument("--phase")
    p.add_argument("--note")
    p.add_argument("raw", nargs="+")
    p = sub.add_parser("unpick")
    p.add_argument("raw", nargs="+")
    p = sub.add_parser("set")
    p.add_argument("--in-pr", required=True, choices=["yes", "no"])
    p.add_argument("targets", nargs="+")
    sub.add_parser("show")
    a = ap.parse_args()
    feat = Feature(a.feature, a.plan)
    m = load(feat)
    {"pick": cmd_pick, "unpick": cmd_unpick, "set": cmd_set, "show": cmd_show}[a.cmd](feat, m, a)
    if a.cmd != "show":
        save(feat, m)


if __name__ == "__main__":
    main()
