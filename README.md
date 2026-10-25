# beeper-line skills

[Agent skills](https://agentskills.io/home) for working on [beeper/line](https://github.com/beeper/line), the Matrix bridge for LINE. They record what the real LINE Chrome Extension does, redact it, compare it with the bridge, and help implement features that match it.

The bridge identifies as the LINE Chrome Extension, so features should copy the extension's captured behavior. These skills are the tooling for that. They run from inside a `beeper/line` checkout and stop if you are somewhere else.

Layout follows [clins1994/skills](https://github.com/clins1994/skills).

## Install

With the [skills CLI](https://github.com/vercel-labs/skills) (any agent):

```bash
npx skills add clins1994/beeper-line-skills                     # pick skills and agents
npx skills add clins1994/beeper-line-skills --skill='*' -g      # all skills, globally
npx skills add clins1994/beeper-line-skills --skill line-implement -a claude-code
```

Install all three (or `line-implement` together with the other two): `line-implement` uses the scripts of `line-capture` and `line-analyze`. Update later with `npx skills update`.

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
| [line-capture](skills/line-capture/SKILL.md) | Checks dependencies, then launches Chrome with a CDP recorder and net-log to record LINE Chrome Extension traffic. Works on macOS, Linux and Windows (Git Bash). |
| [line-analyze](skills/line-analyze/SKILL.md) | Parses a capture, redacts tokens and MIDs, and compares the traffic with `pkg/line` and `pkg/connector`. |

```
line-implement ──► line-capture ──► line-analyze
```

## Requirements

- A checkout (clone, fork or worktree) of `beeper/line`. Run your agent from it.
- Google Chrome (Chromium on Linux), Python 3.8+ and the Python package `websocket-client`. `line-capture` checks these and the agent offers to install what is missing.
- The LINE login is always manual. The skills never ask for, store or automate credentials.

Raw captures contain access tokens, cookies, MIDs and message bodies. Keep them in a temporary folder, redact before you quote anything, and never commit them.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
