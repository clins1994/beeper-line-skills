# Contributing

Thanks for wanting to help. These skills are small on purpose, so most contributions are small too: a sharper rule, a missing case, or support for another platform.

## Using AI

You can use AI to help you contribute. Two rules, adapted from [Anthony Fu's contribution guide](https://github.com/antfu/contribute):

1. **Never let an LLM speak for you.** Write issues, comments and PR descriptions in your own words. Short and plain beats long and polished.
2. **Never let an LLM think for you.** Understand every line you send. Tell us what *you* think, not what a model said.

A pull request that looks fully generated and unreviewed may be closed without discussion.

## Discuss first

For a new skill, or a big change to one, open an issue first. Say what problem it solves and how you would do it. For a typo or a small fix, send the pull request directly.

## How a skill is laid out

```
skills/<name>/
  SKILL.md          # frontmatter (name, description) + the instructions
  REFERENCE.md      # longer detail the agent reads only when it needs it
  scripts/          # helpers the skill runs
```

- Name the folder and `name:` with the `line-` prefix for LINE protocol skills. The plugin adds `beeper-line:`.
- Keep `SKILL.md` short. Move long detail into a reference file.
- Refer to scripts as `<skill-dir>/scripts/<file>`, never as a path inside the bridge repo.
- Start every skill that touches the bridge code with the "Check the checkout first" step.
- Never add captures, tokens, MIDs or Chrome profiles, not even in examples.
- Every skill is listed in the `README.md` table, with its name linked to its `SKILL.md`.

See [`AGENTS.md`](AGENTS.md) for the short version that agents read.

## Before you submit

- [ ] `claude plugin validate .` passes.
- [ ] `bash -n` passes on every shell script and `python3 -m py_compile` on every Python script you touched.
- [ ] `version` in `.claude-plugin/plugin.json` is bumped: minor for a new skill, patch for a fix. Without a bump, installed plugins do not update.
- [ ] The `README.md` table matches the skills.
- [ ] You tried the skill once in a `beeper/line` checkout, and you say in the PR what you tried.

## Commits and pull requests

- Small commits, one change each, with the skill as the prefix: `line-capture: support Chromium on Fedora`. Use `README:`, `plugin:` or no prefix for repo-wide changes.
- Link the issue: `closes #123`.

## License

By contributing, you agree that your contribution is licensed under the [MIT License](LICENSE).
