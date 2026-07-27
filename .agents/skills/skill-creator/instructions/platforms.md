# Platform-Specific Instructions

> Extracted from SKILL.md. Read this when the user is on a specific platform.

## Claude.ai

- **No subagents** — run test cases yourself, one at a time. Skip baselines.
- **No browser** — present results directly in conversation. Save files to filesystem for user to download.
- **No benchmarking** — skip quantitative; focus on qualitative feedback.
- **No description optimization** — requires `claude -p` CLI.
- **No blind comparison** — requires subagents.
- **Packaging works** — `package_skill.py` just needs Python.
- **Updating existing skills** — preserve original name, copy to `/tmp/` first, edit there.

## Cowork

- **Subagents work** — full parallel test workflow supported.
- **No browser** — use `--static <output_path>` for eval viewer. User opens the HTML file.
- **GENERATE THE EVAL VIEWER BEFORE self-evaluating** — get results in front of the human ASAP.
- **Feedback** — "Submit All Reviews" downloads `feedback.json`.
- **Packaging works** — `package_skill.py` needs Python + filesystem.
- **Description optimization** works (uses `claude -p` via subprocess).

## Hermes Desktop (macOS)

- **Subagents work** — delegate_task available.
- **Browser works** — `open` command, `open_preview` tool.
- **Full workflow supported** — parallel tests, viewer, feedback loop.
- **File delivery** — MEDIA: paths for inline rendering.