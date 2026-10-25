---
name: line-test-plan
description: Writes the numbered test plan (PLAN.md) for a beeper/line bridge feature before any capture or code, with lettered sections, step IDs, phases (before, capture, after) and Result columns, plus labeled sample media when the feature needs files. Use when starting a new LINE bridge feature, when asked for a test plan or capture plan, or before running line-capture.
---

# LINE Test Plan

Writes `test/<feature-slug>/PLAN.md` inside a `beeper/line` checkout: the list of
things to do in LINE, Beeper and the Chrome Extension, numbered so every
screenshot, request and result can point at a step. It comes before capture and
code. `<skill-dir>` below is the folder that holds this `SKILL.md`.

## Check the checkout first

Run this from inside a `beeper/line` checkout (or a fork or worktree of it):

```bash
git rev-parse --show-toplevel && grep -E '^module github.com/beeper/line' "$(git rev-parse --show-toplevel)/go.mod"
```

If either command fails, stop. Tell the user to `cd` into their clone of
https://github.com/beeper/line and start again. Do not read or edit any other
repository.

## Contract

Other skills read this layout (`line-evidence` relies on it), so keep it exact.

- Feature folder: `test/<feature-slug>/` in the checkout. `/test` is gitignored there; nothing in it is committed.
- `PLAN.md` holds, in this order:
  1. title, goal, and the issue/PR link
  2. **Scope**: copy the LINE Chrome Extension, nothing extra
  3. **Platforms** involved: Chrome extension, Beeper Desktop, Beeper mobile, LINE iOS, LINE Android
  4. `## Test data`: a bullet per dummy string used in tests (group names, message text, sample file labels). `line-evidence` treats this as the allowlist of text that is not PII
  5. `## Run order`: which sections run in which phase
  6. lettered sections `## A. Title`, each with one table
  7. `## Findings`: a link to `FINDINGS.md` (the agent writes it in the analyze phase, after `line-analyze` has parsed the capture; the plan only links to it)
- Step IDs match `^[A-Z][0-9]+$` (`A1`, `B12`) and are unique across the plan.
- Every table has exactly these columns: `#`, `Platform`, `Phase`, `Action`, `Checks`, `Evidence`, `Result`.
  - `Phase` is `before`, `capture` or `after`.
  - `Evidence` names the screenshots and requests the step should produce, for example `shot: Beeper shows the GIF; req: sendMessage`.
  - `Result` starts empty.
- Sample media lives in `test/<feature-slug>/samples/`.

[TEMPLATE.md](TEMPLATE.md) is a skeleton with every part.

## What to do

1. **Ask for the goal and the issue or PR.** One question: the feature in a
   sentence, and the `beeper/line` issue or PR number (read it with `gh issue
   view` / `gh pr view`). Pick a short `<feature-slug>` (`group-avatar`,
   `send-gifs`) and confirm it.

2. **Read what exists, then propose.**
   - `AGENTS.md`/`CLAUDE.md`, `docs/protocol/`, and the code the feature touches in `pkg/line/` and `pkg/connector/`.
   - Every `test/*/FINDINGS.md` of related features: what the extension already
     enforces (limits, formats, rules) tells you which cases are known and which
     still need a capture.
   - Then show the user the proposed sections as a short list (letter, title,
     phase, platform, number of steps) and let them add, drop or reorder before
     you write steps. Do not write the full plan first.

3. **Sections to propose.** Always include:
   - **Beeper baseline** (`before`): how the feature behaves today through the bridge, so "after" has something to compare with.
   - **Sending from Chrome** (`capture`): one step per variant the extension offers.
   - **Changes made on another device** (`capture`): the user does it in LINE on their phone while the extension stays open; this is what the bridge receives. Include LINE iOS and Android if both are available. Add a step for "undo it" so the test chat is tidy.
   - **Edge cases** (`capture`): limits (length, size, count), empty or unchanged input, cancel before sending, unsupported formats (greyed out in a picker is a result too), unicode and emoji, group vs. 1:1 chat, Letter Sealing on vs. off.
   - **Beeper after deploy** (`after`): the same actions as the baseline, plus the edge cases that matter, plus changes made on LINE iOS/Android arriving in Beeper (Desktop and mobile).
   - Add sections the feature needs (media formats, reactions, permissions). Cover only what the extension does.
   - Prefer one phase per section. If a topic spans phases, split it into two sections and cross-reference them.

4. **Order the phases around the single Chrome Extension session.** LINE allows
   one extension session at a time, so a capture logs the bridge out (and
   running the bridge logs the capture out).
   1. `before`: Beeper steps, bridge logged in.
   2. `capture`: the user logs the bridge out, starts `line-capture`, and does every Chrome step and every other-device step without breaking the session; then quits Chrome.
   3. `after`: the feature is deployed, the bridge is logged in again, and the Beeper steps run on the new build.
   Write this into `## Run order` (phase → sections). Within a table, rows follow the order the user performs them.

5. **Write the steps.** Each one is a single action a person can do in about 10
   seconds, with a `Checks` cell that says what the step is for ("which
   attribute flag", "is the 60-character name cut?") and an `Evidence` cell with
   the expected screenshot or request. Use only dummy strings, and list every
   one in `## Test data`. Never put real names, MIDs, phone numbers or tokens
   in the plan.

6. **Sample media, when the feature needs files.**
   - Run `bash <skill-dir>/scripts/line-test-plan-preflight.sh` (on Windows, from Git Bash). It prints `OK`, `MISSING` (required) or `OPTIONAL` per dependency and does not say how to install anything: choose the install method that fits the detected OS and package managers (for example `<python> -m pip install --user Pillow`), show the commands, ask the user to confirm, install, and re-run until it exits 0.
   - Use the Python the preflight found (`py -3` on Windows only; a `PYTHON` override is respected): `eval "$(bash <skill-dir>/scripts/line-test-plan-preflight.sh --print-env)"` sets the `PYTHON` array, and the commands below run it as `"${PYTHON[@]}"`.
   - Generate labeled samples:
     ```bash
     "${PYTHON[@]}" <skill-dir>/scripts/make-samples.py test/<feature-slug>/samples --kinds image,animated
     ```
     `--kinds` takes `image`, `animated`, `video`, `shape`; `--only 10,21` picks files by number. Every file shows its own name and corner markers, so a screenshot proves which file was sent and how it was cropped.
   - It runs on macOS, Linux and Windows with Python 3.8+ and Pillow. Video (MP4, HEVC, MOV, WebM) needs `ffmpeg`; HEIC and AVIF need `pillow-heif` or an `ffmpeg` with the encoder. Whatever it cannot encode is listed as skipped: tell the user, and do not put those files in the plan.
   - Put each file name in the plan's steps and its label (from `samples/MANIFEST.txt`) in `## Test data`.

7. **Validate and hand over.** Run `"${PYTHON[@]}" <skill-dir>/scripts/check-plan.py test/<feature-slug>/PLAN.md` (set `PYTHON` as in step 6; do it here too if the feature has no media) and fix what it reports. Then tell the user how to run it:
   - **Pacing:** do one step, wait about 10 seconds, then the next. The gaps let the analysis match each step to its network calls. Other-device steps need about 15 seconds before the next one.
   - **Result column:** say it as you go ("A3 saved", "B4 greyed out", "C2 error: ..."). Mark `✅` accepted or working, `❌` rejected or broken (copy the error text), `n/a` with the reason when the step cannot be done, and add notes on cropping, animation or timing.
   - **Order:** all `before` steps, then log the bridge out and start the capture for the `capture` steps, then deploy and run the `after` steps.

8. **Fill results as the user reports them.** When the user says what happened,
   edit the matching `Result` cell right away, with the step ID. If a report
   does not match any step, ask. Keep errors verbatim, and leave a step empty
   rather than guessing. When the plan is finished, point to `line-capture` for
   the capture phase and `line-analyze` to parse it; the agent then writes `FINDINGS.md` from that analysis.

Never commit the feature folder, and keep captures, tokens, MIDs and real
account data out of the plan.
