# beeper-line skills

[Agent skills](https://agentskills.io/home) for working on [beeper/line](https://github.com/beeper/line), the Matrix bridge for LINE. They record what the real LINE Chrome Extension does, redact it, compare it with the bridge, and help implement features that match it.

These skills are completely optional. They are my own way of working on the bridge, kept here so I can change them on my own schedule, and `beeper/line` does not need them. If you want help reverse engineering what the LINE Chrome Extension does, and later an opinionated way to structure the evidence for that kind of work, you can try them. The bridge identifies as the extension, so features should copy its captured behavior; these skills are tooling for that. They run from inside a `beeper/line` checkout and stop if you are somewhere else.

Layout follows [clins1994/skills](https://github.com/clins1994/skills).

## Install

With the [skills CLI](https://github.com/vercel-labs/skills) (any agent):

```bash
npx skills add clins1994/beeper-line-skills                     # pick skills and agents
npx skills add clins1994/beeper-line-skills --skill='*' -g      # all skills, globally
npx skills add clins1994/beeper-line-skills --skill line-implement -a claude-code
```

Install `line-implement` together with `line-capture` and `line-analyze`: it uses their scripts. `line-test-plan` works on its own. Update later with `npx skills update`.

As a Claude Code plugin (updates with `claude plugin update`):

```
/plugin marketplace add clins1994/beeper-line-skills
/plugin install beeper-line@beeper-line-skills
```

The plugin names each skill `beeper-line:<skill>`, for example `/beeper-line:line-capture`. The skills CLI installs it as `line-capture`.

## Skills

| Skill | What it does |
|-------|--------------|
| [line-implement](skills/line-implement/SKILL.md) | The umbrella. Turns a feature goal into a capture contract, captures only the missing evidence, then implements the bridge to match Chrome. Uses the two skills below. |
| [line-test-plan](skills/line-test-plan/SKILL.md) | Writes the numbered test plan (`test/<feature>/PLAN.md`) before any capture or code: sections, step IDs, before/capture/after phases, Result column, and labeled sample media when the feature needs files. Works on macOS, Linux and Windows (Git Bash). |
| [line-capture](skills/line-capture/SKILL.md) | Checks dependencies, then launches Chrome with a CDP recorder and net-log to record LINE Chrome Extension traffic. Works on macOS, Linux and Windows (Git Bash). |
| [line-analyze](skills/line-analyze/SKILL.md) | Parses a capture, redacts tokens and MIDs, and compares the traffic with `pkg/line` and `pkg/connector`. |
| [line-evidence](skills/line-evidence/SKILL.md) | Turns a feature's test screenshots into PR-ready evidence: collects them, lets you pick from a local contact sheet, covers names, faces, phone numbers, emails and MIDs found with on-device OCR, and writes approved, metadata-free PNGs plus a manifest. Raw screenshots never leave the machine. |

```
line-implement ──► line-test-plan (optional)
               ──► line-capture ──► line-analyze
```

## Requirements

- A checkout (clone, fork or worktree) of `beeper/line`. Run your agent from it.
- Google Chrome (Chromium on Linux), Python 3.8+ and the Python package `websocket-client`. `line-capture` checks these and the agent offers to install what is missing.
- `line-evidence` needs Python 3.8+ with Pillow, and an OCR engine: Apple Vision on macOS (through `swiftc`), tesseract elsewhere. Its preflight checks these.
- The LINE login is always manual. The skills never ask for, store or automate credentials.

Raw captures contain access tokens, cookies, MIDs and message bodies. Keep them in a temporary folder, redact before you quote anything, and never commit them.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
