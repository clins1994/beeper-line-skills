Skills live one per folder under `skills/` (`skills/<name>/SKILL.md`). Claude Code loads them through the `beeper-line` plugin (`.claude-plugin/plugin.json`, listed in `.claude-plugin/marketplace.json`), and `npx skills` finds the same folders.

These skills are for working on [beeper/line](https://github.com/beeper/line), the Matrix bridge for LINE. They run from inside a checkout of that repo and stop clearly when they are not. Each one starts with a "Check the checkout first" step; keep it in every new skill that touches the bridge code.

Name a skill's folder and its `name:` with the `line-` prefix for LINE protocol skills (`skills/line-capture/`, `name: line-capture`), so they do not clash with other skills when installed with `npx skills`. The plugin adds its own prefix: Claude Code shows the skill as `/beeper-line:line-capture`. When one skill refers to another, write the plain name (`line-analyze`).

Put a skill's scripts in `skills/<name>/scripts/` and refer to them in docs as `<skill-dir>/scripts/<file>`, where `<skill-dir>` is the folder holding that `SKILL.md`. Never assume a script sits inside the repo being worked on. A skill that needs a sibling's script uses `<skill-dir>/../<sibling>/scripts/<file>`.

Every skill must be listed in the top-level `README.md`, with its name linked to its `SKILL.md`.

Keep skills free of secrets and personal data: no tokens, MIDs, captures or Chrome profiles. Captures are always redacted before anything is quoted.

Check shell scripts with `bash -n` and Python scripts with `python3 -m py_compile` before you commit.

Run `claude plugin validate .` after you add a skill or change a manifest.

Bump `version` in `.claude-plugin/plugin.json` in every PR that changes a skill or a manifest. Use semver: a minor bump for a new skill, a patch bump for fixes. `claude plugin update` compares this version, so without a bump installed copies do not update.
