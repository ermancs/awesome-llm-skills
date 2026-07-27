#!/usr/bin/env python3
"""new_skill.py — Gold Standard (Altın Standart) skill scaffold generator.

Scaffolds a complete 10-directory skill skeleton with all required files:
  SKILL.md + manifest.json + README.md + LICENSE + CHANGELOG.md +
  instructions/ + tools/ + examples/ + tests/ + config/ + src/ +
  data/ + scripts/ + errors/

Every placeholder is marked [[FILL: ...]] for the author to replace.

Usage:
  python new_skill.py "<skill-name>" [--description "one-line intent"]
                      [--dest DIR] [--force] [--minimal] [--legacy]

Examples:
  python new_skill.py sozlesme-ozetleyici \
      --description "Türkçe sözleşmeleri madde madde özetler"
  python new_skill.py invoice-linter --dest ./output
  python new_skill.py quick-helper --minimal   # only SKILL.md + manifest + CHANGELOG
  python new_skill.py old-style --legacy       # old 7-pillar format (v1.x compat)
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

DEFAULT_DEST = str(Path.home() / ".hermes" / "skills")


def _today(explicit: str | None) -> str:
    if explicit:
        return explicit
    return datetime.date.today().isoformat()


def slugify(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    if not s:
        raise ValueError("Skill name reduces to empty after slugifying.")
    return s


def title_case(slug: str) -> str:
    return " ".join(w.capitalize() for w in slug.split("-"))


# ═══════════════════════════════════════════════════════════════════════════
# Gold Standard Templates
# ═══════════════════════════════════════════════════════════════════════════

SKILL_MD = """---
name: {slug}
description: >-
  {desc} Make sure to use this skill whenever the user
  [[FILL: list the concrete phrasings, contexts, and file types that should
  trigger it — include casual wording and near-synonyms]]. Be a little pushy:
  trigger even when the user does not name the skill but clearly needs it.
  Do NOT use this skill for [[FILL: adjacent task]] — use
  [[FILL: sibling-skill]] instead.
version: 0.1.0
author: {author}
license: MIT
metadata:
  hermes:
    tags: [[FILL: tag1, tag2]]
    related_skills: [[FILL: related-skill-name]]
---

# {title}

[[FILL: one or two sentences on what this skill does and the outcome the user
gets. Explain the *why* so the model applies judgment rather than following
rote steps.]]

## When to use

[[FILL: the trigger conditions in prose — mirror the description but with a
little more nuance and examples of real user phrasings.]]

## Workflow

1. [[FILL: first step — usually gather/resolve inputs.]]
2. [[FILL: the core step. If any step is repetitive, error-prone by hand, or
   must be byte-identical every run, run the deterministic helper instead of
   doing it inline:]]
   ```bash
   python scripts/run.py [[FILL: args]]
   ```
3. [[FILL: format the output using the canonical template so the shape never
   drifts run to run:]] `data/templates/output.md`.

## Output format

ALWAYS follow `data/templates/output.md`. [[FILL: or inline the exact skeleton
here if it is short.]]

## When NOT to use this skill (scope guard)

- **[[FILL: adjacent task A]]** → use `[[FILL: sibling-skill-A]]`.
- **[[FILL: adjacent task B]]** → use `[[FILL: sibling-skill-B]]`.
- [[FILL: any read-only / built-in boundary, destructive-action caveat, etc.]]

## Reference files

- `instructions/system.md` — [[FILL: role and capabilities; read when unsure about scope]].
- `instructions/constraints.md` — [[FILL: what this skill must NOT do]].
- `instructions/style.md` — [[FILL: language, tone, format conventions]].
- `data/knowledge/reference.md` — [[FILL: deep domain detail; read when …]].
- `data/templates/output.md` — the canonical output shape.
- `tests/eval/evals.json` — test prompts; hand to `skill-creator` to benchmark.
- `errors/error_codes.json` — structured error catalog with fallback actions.
- `config/default.yaml` — runtime parameters and safety boundaries.
- `CHANGELOG.md` — history of what changed and why.
"""

MANIFEST_JSON = """{{
  "id": "{slug}",
  "name": "{title}",
  "version": "0.1.0",
  "author": "{author}",
  "license": "MIT",
  "runtime": {{
    "min_model_tier": "[[FILL: sonnet-class | opus-class | haiku-class]]",
    "context_window_required": "[[FILL: 32000]]",
    "languages": "[[FILL: [\\\"tr\\\", \\\"en\\\"]]]"
  }},
  "entry_point": "src/main.py",
  "tools": "[[FILL: tool schemas — see tools/*.json]]",
  "dependencies": {{
    "python": ">=3.11",
    "packages": "[[FILL: [\\\"pandas>=2.0\\\"]]]"
  }},
  "evals": {{
    "pass_rate": "[[FILL: null or 0.95]]",
    "last_run": "[[FILL: null or \\\"2026-07-26\\\"]]"
  }},
  "tags": "[[FILL: [\\\"tag1\\\", \\\"tag2\\\"]]]",
  "security": {{
    "allow_network": "[[FILL: false]]",
    "allow_file_write": "[[FILL: true]]",
    "blocked_paths": "[[FILL: [\\\"/etc\\\", \\\"/sys\\\", \\\"~/.ssh\\\"]]]",
    "max_cost_per_call": "[[FILL: 5.0]]"
  }}
}}
"""

README_MD = """# {title}

> **Skill ID:** `{slug}` | **Version:** 0.1.0 | **Author:** {author}

[[FILL: One-paragraph overview of what this skill does and who it's for.]]

## Quick Start

1. [[FILL: Step 1 — e.g., "Provide a CSV file"]]
2. [[FILL: Step 2 — e.g., "Ask: 'analyze this data'"]]
3. [[FILL: Step 3 — e.g., "Review the summary and charts"]]

## What It Does

[[FILL: Detailed capabilities list.]]

## What It Doesn't Do

[[FILL: Scope limitations.]]

## Dependencies

- Python >= 3.11
- [[FILL: additional packages]]

## Configuration

See `config/default.yaml` for runtime parameters and `config/schema.json` for
the configuration schema.

## Testing

```bash
pytest tests/
```

## License

MIT — see `LICENSE` file.
"""

LICENSE_TEXT = """MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

CHANGELOG_MD = """# Changelog

All notable changes to the **{slug}** skill are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/); this skill uses
[Semantic Versioning](https://semver.org/).

## [0.1.0] — {date}

### Added
- Scaffolded from the Gold Standard `skill-creator` v2.0.0: 10-directory
  structure (SKILL.md + manifest.json + instructions/tools/examples/tests/
  config/src/data/scripts/errors).

### TODO before first real use
- Replace every `[[FILL: …]]` placeholder in all files.
- Flesh out `src/main.py` and `scripts/run.py` (or delete if unused).
- Write real eval prompts + assertions in `tests/eval/evals.json`.
- Fill the canonical output shape in `data/templates/output.md`.
- Add real examples to `examples/`.
"""

# --- instructions/ ---

SYSTEM_MD = """# {title} — System Prompt

[[FILL: The system-level prompt for this skill. Defines:
- Agent role and persona
- Core capabilities
- Available tools
- Expected behavior]]

## Role

[[FILL: e.g., "You are an expert data analyst specializing in..." ]]

## Capabilities

[[FILL: What this skill enables the agent to do.]]

## Tools at Your Disposal

[[FILL: List of tools with brief descriptions.]]
"""

CONSTRAINTS_MD = """# {title} — Constraints

[[FILL: Hard boundaries and rules. What the agent must NEVER do.]]

## Absolute Constraints

- [[FILL: Constraint 1]]
- [[FILL: Constraint 2]]

## Data Boundaries

- **Max input size:** [[FILL: e.g., 100MB]]
- **Allowed file types:** [[FILL: e.g., CSV, Excel, JSON]]
- **Blocked paths:** [[FILL: from config/default.yaml → safety.blocked_paths]]

## Cost Limits

- **Max cost per call:** [[FILL: from manifest.json → security.max_cost_per_call]]
- **Max iterations:** [[FILL: from config/default.yaml]]

## Network

- **Allow network:** [[FILL: true/false]]
"""

STYLE_MD = """# {title} — Output Style

[[FILL: Defines the language, tone, and format conventions for outputs.]]

## Language

[[FILL: e.g., Turkish (tr), English (en), or both]]

## Tone

[[FILL: e.g., Professional, direct, clinical, friendly]]

## Format

[[FILL: e.g., Markdown with specific section structure]]

## Conventions

- [[FILL: Convention 1 — e.g., "Use bullet points for findings"]]
- [[FILL: Convention 2 — e.g., "Include confidence scores"]]
- [[FILL: Convention 3 — e.g., "Never use emojis in analysis output"]]
"""

# --- tools/ ---

TOOL_SCHEMA_JSON = """{{
  "name": "[[FILL: tool_name]]",
  "description": "[[FILL: What this tool does]]",
  "parameters": {{
    "type": "object",
    "properties": {{
      "[[FILL: param_name]]": {{
        "type": "[[FILL: string | number | boolean | array | object]]",
        "description": "[[FILL: Parameter description]]"
      }}
    }},
    "required": [[FILL: ["param_name"]]]
  }},
  "returns": {{
    "type": "object",
    "properties": {{
      "[[FILL: result_field]]": {{
        "type": "[[FILL: string | number]]",
        "description": "[[FILL: Description]]"
      }}
    }}
  }},
  "errors": [[FILL: ["ERROR_CODE_1", "ERROR_CODE_2"]]]
}}
"""

SCHEMAS_PY = """#!/usr/bin/env python3
\"\"\"Tool schemas for the {slug} skill.

Define function-calling schemas as Python dicts for runtime use.
Mirrors tools/*.json — keep them in sync.
\"\"\"

from __future__ import annotations

# [[FILL: Define your tool schemas here]]
TOOLS: list[dict] = []
"""

# --- examples/ ---

EXAMPLE_BASIC = """# Example: Basic Usage

## Scenario
[[FILL: A straightforward, common use case.]]

## User Prompt
```
[[FILL: What the user actually types.]]
```

## Expected Behavior
1. [[FILL: Step 1]]
2. [[FILL: Step 2]]
3. [[FILL: Step 3]]

## Expected Output
```
[[FILL: What the agent should produce.]]
```
"""

EXAMPLE_EDGE = """# Example: Edge Case — [[FILL: edge case name]]

## Scenario
[[FILL: A challenging or boundary case, e.g., missing data, very large input,
ambiguous request.]]

## User Prompt
```
[[FILL: What the user types.]]
```

## Expected Behavior
1. [[FILL: Step 1 — detection]]
2. [[FILL: Step 2 — handling]]
3. [[FILL: Step 3 — fallback]]

## Expected Output
```
[[FILL: What the agent should produce, including error handling.]]
```
"""

EXAMPLE_CONVERSATIONAL = """# Example: Conversational Flow

## Scenario
[[FILL: A multi-turn conversation showing the skill in context.]]

## Trace
```
[kullanıcı]: [[FILL: First user message]]
[ajan]: [[FILL: Agent response]]
[kullanıcı]: [[FILL: Follow-up]]
[ajan]: [[FILL: Agent response with skill output]]
```
"""

# --- tests/ ---

TEST_INIT = """# {slug} — Test package
"""

EVALS_JSON = """{{
  "skill_name": "{slug}",
  "evals": [
    {{
      "id": 1,
      "prompt": "[[FILL: a realistic prompt a real user would type that SHOULD trigger and exercise this skill.]]",
      "expected_output": "[[FILL: what a good result looks like.]]",
      "files": [],
      "assertions": [
        {{
          "name": "produces_expected_artifact",
          "text": "[[FILL: objective, verifiable check — e.g. 'output file exists and has N sections'.]]"
        }}
      ]
    }},
    {{
      "id": 2,
      "prompt": "[[FILL: a second realistic prompt, phrased differently / a harder case.]]",
      "expected_output": "[[FILL: expected result.]]",
      "files": [],
      "assertions": [
        {{
          "name": "[[FILL: assertion name]]",
          "text": "[[FILL: objective check.]]"
        }}
      ]
    }},
    {{
      "id": 3,
      "prompt": "[[FILL: an edge / near-miss case that helps tune triggering and scope.]]",
      "expected_output": "[[FILL: expected result.]]",
      "files": [],
      "assertions": []
    }}
  ]
}}
"""

# --- config/ ---

DEFAULT_YAML = """# {title} — Default Configuration
# See config/schema.json for the full schema.

skill:
  name: {slug}
  max_iterations: [[FILL: 5]]
  timeout_seconds: [[FILL: 30]]

sampling:
  default_size: [[FILL: 1000]]
  max_size: [[FILL: 100000]]

output:
  max_recommendations: [[FILL: 5]]
  language: [[FILL: tr]]
  format: [[FILL: markdown]]

safety:
  allow_network: false
  allow_file_write: true
  blocked_paths:
    - /etc
    - /sys
    - ~/.ssh
  max_cost_per_call: 5.0
"""

CONFIG_SCHEMA_JSON = """{{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "{title} Configuration Schema",
  "type": "object",
  "properties": {{
    "skill": {{
      "type": "object",
      "properties": {{
        "name": {{ "type": "string" }},
        "max_iterations": {{ "type": "integer", "minimum": 1 }},
        "timeout_seconds": {{ "type": "integer", "minimum": 1 }}
      }},
      "required": ["name"]
    }},
    "output": {{
      "type": "object",
      "properties": {{
        "max_recommendations": {{ "type": "integer", "minimum": 1 }},
        "language": {{ "type": "string" }},
        "format": {{ "type": "string", "enum": ["markdown", "json", "text"] }}
      }}
    }},
    "safety": {{
      "type": "object",
      "properties": {{
        "allow_network": {{ "type": "boolean" }},
        "allow_file_write": {{ "type": "boolean" }},
        "blocked_paths": {{ "type": "array", "items": {{ "type": "string" }} }},
        "max_cost_per_call": {{ "type": "number", "minimum": 0 }}
      }}
    }}
  }}
}}
"""

# --- src/ ---

MAIN_PY = """#!/usr/bin/env python3
\"\"\"main.py — Entry point for the {slug} skill.

This is the primary executable logic. The skill's SKILL.md tells the agent
when to call this; the logic lives here so it is written once and cannot drift.
\"\"\"

from __future__ import annotations

import argparse
import sys


def run(args: argparse.Namespace) -> int:
    # [[FILL: Real logic goes here.]]
    print(f"[{slug}] main.py stub — implement me. input={{args.input!r}}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="{title} — main entry point.")
    parser.add_argument("--input", help="[[FILL: describe the input.]]")
    args = parser.parse_args(argv)
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
"""

UTILS_PY = """#!/usr/bin/env python3
\"\"\"utils.py — Shared utilities for the {slug} skill.\"\"\"

from __future__ import annotations

# [[FILL: Shared helper functions go here.]]
"""

# --- data/ ---

OUTPUT_TEMPLATE_MD = """<!-- Canonical output shape for the {slug} skill. -->
<!-- The skill fills this in every run so the format never drifts. -->

# [[FILL: Title / subject]]

## [[FILL: Section 1]]
[[FILL: content]]

## [[FILL: Section 2]]
[[FILL: content]]

## [[FILL: Section 3 — e.g. action items / recommendations, if relevant]]
[[FILL: content]]
"""

REFERENCE_MD = """# {title} — Reference

> Load-on-demand detail for the `{slug}` skill (progressive disclosure).
> SKILL.md stays lean; the heavy material lives here and is read only when needed.

## Table of contents
- [Background](#background)
- [Details / variants](#details--variants)
- [Edge cases](#edge-cases)
- [Worked example](#worked-example)

## Background
[[FILL: the domain knowledge the model needs but that would bloat SKILL.md.]]

## Details / variants
[[FILL: per-variant or per-framework specifics. If this skill supports several
domains, give each its own section here so the model reads only the relevant
one.]]

## Edge cases
[[FILL: the tricky inputs and how to handle them.]]

## Worked example
[[FILL: one concrete input -> output walk-through.]]
"""

# --- scripts/ ---

RUN_PY = """#!/usr/bin/env python3
\"\"\"run.py — Deterministic helper for the {slug} skill.

Put here any step that is repetitive, error-prone to do by hand, or that must
produce byte-identical output every run (parsing, formatting, arithmetic, file
generation). The SKILL.md tells the model *when* to call this; the logic lives
here so it is written once and cannot drift.
\"\"\"

from __future__ import annotations

import argparse
import sys


def run(args: argparse.Namespace) -> int:
    # [[FILL: real deterministic logic goes here.]]
    print(f"[{slug}] run.py stub — implement me. input={{args.input!r}}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Deterministic helper for {slug}.")
    parser.add_argument("--input", help="[[FILL: describe the input.]]")
    args = parser.parse_args(argv)
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
"""

VALIDATE_PY = """#!/usr/bin/env python3
\"\"\"validate.py — Validate the {slug} skill structure and integrity.\"\"\"

from __future__ import annotations

import sys
from pathlib import Path


def validate(skill_path: Path) -> list[str]:
    \"\"\"Run all validation checks. Returns list of issues (empty = valid).\"\"\"
    issues: list[str] = []

    # Check required files
    required = ["SKILL.md", "manifest.json", "CHANGELOG.md", "LICENSE", "README.md"]
    for f in required:
        if not (skill_path / f).exists():
            issues.append(f"Missing required file: {{f}}")

    # Check required directories
    required_dirs = [
        "instructions", "tools", "examples", "tests",
        "config", "src", "data", "scripts", "errors"
    ]
    for d in required_dirs:
        if not (skill_path / d).is_dir():
            issues.append(f"Missing required directory: {{d}}/")

    # [[FILL: Add domain-specific validation checks here.]]

    return issues


def main(argv: list[str] | None = None) -> int:
    path = Path(argv[0]) if argv else Path.cwd()
    issues = validate(path)
    if issues:
        print(f"❌ {{len(issues)}} validation issue(s):")
        for i in issues:
            print(f"  - {{i}}")
        return 1
    print(f"✅ Skill at {{path}} is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
"""

BENCHMARK_PY = """#!/usr/bin/env python3
\"\"\"benchmark.py — Run benchmarks for the {slug} skill.\"\"\"

from __future__ import annotations

import sys


def main(argv: list[str] | None = None) -> int:
    # [[FILL: Benchmark logic — run evals, measure pass_rate, latency, tokens.]]
    print(f"[{slug}] benchmark.py stub — implement me.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
"""

# --- errors/ ---

ERROR_CODES_JSON = """{{
  "[[FILL: ERROR_CODE_1]]": {{
    "user_message": "[[FILL: User-facing message with {{param}} placeholders]]",
    "retry": false,
    "fallback_action": "[[FILL: ask_user_for_input | use_default | skip | abort]]",
    "severity": "[[FILL: error | warning | info]]"
  }},
  "[[FILL: ERROR_CODE_2]]": {{
    "user_message": "[[FILL: User-facing message]]",
    "retry": true,
    "fallback_action": "[[FILL: exponential_backoff | retry_with_backoff]]",
    "severity": "[[FILL: error | warning]]"
  }}
}}
"""


# ═══════════════════════════════════════════════════════════════════════════
# Legacy 7-pillar templates (--legacy flag)
# ═══════════════════════════════════════════════════════════════════════════

LEGACY_SKILL_MD = """---
name: {slug}
description: >-
  {desc} Make sure to use this skill whenever the user
  [[FILL: list the concrete phrasings, contexts, and file types that should
  trigger it — include casual wording and near-synonyms, e.g. "do X", "handle
  the Y file", "prepare a Z"]]. Be a little pushy: trigger even when the user
  does not say the skill's name explicitly but clearly needs it. Do NOT use this
  skill for [[FILL: the adjacent task a sibling skill owns]] — use
  [[FILL: sibling-skill]] instead.
---

# {title}

[[FILL: one or two sentences on what this skill does and the outcome the user
gets. Explain the *why* so the model applies judgment rather than following
rote steps.]]

## When to use

[[FILL: the trigger conditions in prose — mirror the description but with a
little more nuance and examples of real user phrasings.]]

## Workflow

1. [[FILL: first step — usually gather/resolve inputs.]]
2. [[FILL: the core step. If any step is repetitive, error-prone by hand, or
   must be byte-identical every run, run the deterministic helper instead of
   doing it inline:]]
   ```bash
   python scripts/run.py [[FILL: args]]
   ```
3. [[FILL: format the output using the canonical template so the shape never
   drifts run to run:]] `assets/templates/output.md`.

## Output format

ALWAYS follow `assets/templates/output.md`. [[FILL: or inline the exact skeleton
here if it is short.]]

## When NOT to use this skill (scope guard)

- **[[FILL: adjacent task A]]** → use `[[FILL: sibling-skill-A]]`.
- **[[FILL: adjacent task B]]** → use `[[FILL: sibling-skill-B]]`.
- [[FILL: any read-only / built-in boundary, destructive-action caveat, etc.]]

## Reference files

- `references/reference.md` — [[FILL: what deep detail lives there; read it
  when …]]. Keep this SKILL.md lean and push long tables / per-variant docs
  into references (progressive disclosure).
- `assets/templates/output.md` — the canonical output shape.
- `evals/evals.json` — test prompts for this skill; hand to `skill-creator` to
  run the benchmark/iteration loop.
- `CHANGELOG.md` — history of what changed and why.
"""

LEGACY_CHANGELOG_MD = """# Changelog

All notable changes to the **{slug}** skill are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/); this skill uses
[Semantic Versioning](https://semver.org/).

## [0.1.0] — {date}

### Added
- Scaffolded from the 7-pillar `skill-creator` standard: pushy description,
  progressive disclosure (SKILL.md + references/), deterministic script
  (scripts/run.py), CHANGELOG, eval set (evals/evals.json), output template
  (assets/templates/output.md), and a scope guard.

### TODO before first real use
- Replace every `[[FILL: …]]` placeholder in SKILL.md.
- Flesh out `scripts/run.py` (or delete it if the skill needs no deterministic
  step).
- Write real eval prompts + assertions in `evals/evals.json`.
- Fill the canonical output shape in `assets/templates/output.md`.
"""

LEGACY_RUN_PY = RUN_PY  # Same content

LEGACY_REFERENCE_MD = REFERENCE_MD  # Same content

LEGACY_OUTPUT_TEMPLATE_MD = OUTPUT_TEMPLATE_MD  # Same content


def legacy_evals_json(slug: str) -> str:
    payload = {
        "skill_name": slug,
        "evals": [
            {
                "id": 1,
                "prompt": "[[FILL: a realistic prompt a real user would type "
                          "that SHOULD trigger and exercise this skill.]]",
                "expected_output": "[[FILL: what a good result looks like.]]",
                "files": [],
                "assertions": [
                    {
                        "name": "produces_expected_artifact",
                        "text": "[[FILL: objective, verifiable check — e.g. "
                                "'output file exists and has N sections'.]]",
                    }
                ],
            },
            {
                "id": 2,
                "prompt": "[[FILL: a second realistic prompt, phrased "
                          "differently / a harder case.]]",
                "expected_output": "[[FILL: expected result.]]",
                "files": [],
                "assertions": [
                    {
                        "name": "[[FILL: assertion name]]",
                        "text": "[[FILL: objective check.]]",
                    }
                ],
            },
            {
                "id": 3,
                "prompt": "[[FILL: an edge / near-miss case that helps you tune "
                          "triggering and scope.]]",
                "expected_output": "[[FILL: expected result.]]",
                "files": [],
                "assertions": [],
            },
        ],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


# ═══════════════════════════════════════════════════════════════════════════
# File writer
# ═══════════════════════════════════════════════════════════════════════════

def write_file(path: Path, content: str, force: bool) -> str:
    if path.exists() and not force:
        return f"skip (exists): {path}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"wrote: {path}"


# ═══════════════════════════════════════════════════════════════════════════
# Scaffolders
# ═══════════════════════════════════════════════════════════════════════════

def scaffold_gold(slug: str, title: str, desc: str, author: str,
                  dest: Path, force: bool, date: str) -> list[str]:
    """Scaffold the full Gold Standard 10-directory structure."""
    root = dest / slug
    fills = dict(slug=slug, title=title, desc=desc.strip(),
                 author=author, date=date, year=date[:4])
    results: list[str] = []

    # ── Root files ──
    results.append(write_file(root / "SKILL.md", SKILL_MD.format(**fills), force))
    results.append(write_file(root / "manifest.json", MANIFEST_JSON.format(**fills), force))
    results.append(write_file(root / "README.md", README_MD.format(**fills), force))
    results.append(write_file(root / "LICENSE", LICENSE_TEXT.format(**fills), force))
    results.append(write_file(root / "CHANGELOG.md", CHANGELOG_MD.format(**fills), force))

    # ── instructions/ ──
    results.append(write_file(root / "instructions" / "system.md", SYSTEM_MD.format(**fills), force))
    results.append(write_file(root / "instructions" / "constraints.md", CONSTRAINTS_MD.format(**fills), force))
    results.append(write_file(root / "instructions" / "style.md", STYLE_MD.format(**fills), force))

    # ── tools/ ──
    results.append(write_file(root / "tools" / "tool_1.json", TOOL_SCHEMA_JSON.format(**fills), force))
    results.append(write_file(root / "tools" / "tool_2.json", TOOL_SCHEMA_JSON.format(**fills), force))
    results.append(write_file(root / "tools" / "schemas.py", SCHEMAS_PY.format(**fills), force))

    # ── examples/ ──
    results.append(write_file(root / "examples" / "basic" / "example_01.md", EXAMPLE_BASIC.format(**fills), force))
    results.append(write_file(root / "examples" / "edge_cases" / "missing_data.md", EXAMPLE_EDGE.format(**fills), force))
    results.append(write_file(root / "examples" / "conversational" / "example_01.md", EXAMPLE_CONVERSATIONAL.format(**fills), force))

    # ── tests/ ──
    results.append(write_file(root / "tests" / "unit" / "__init__.py", TEST_INIT.format(**fills), force))
    results.append(write_file(root / "tests" / "integration" / "__init__.py", TEST_INIT.format(**fills), force))
    results.append(write_file(root / "tests" / "eval" / "evals.json", EVALS_JSON.format(**fills), force))
    results.append(write_file(root / "tests" / "fixtures" / ".gitkeep", "", force))

    # ── config/ ──
    results.append(write_file(root / "config" / "default.yaml", DEFAULT_YAML.format(**fills), force))
    results.append(write_file(root / "config" / "production.yaml", DEFAULT_YAML.format(**fills), force))
    results.append(write_file(root / "config" / "schema.json", CONFIG_SCHEMA_JSON.format(**fills), force))

    # ── src/ ──
    results.append(write_file(root / "src" / "main.py", MAIN_PY.format(**fills), force))
    results.append(write_file(root / "src" / "utils.py", UTILS_PY.format(**fills), force))
    results.append(write_file(root / "src" / "handlers" / "__init__.py", TEST_INIT.format(**fills), force))

    # ── data/ ──
    results.append(write_file(root / "data" / "templates" / "output.md", OUTPUT_TEMPLATE_MD.format(**fills), force))
    results.append(write_file(root / "data" / "knowledge" / "reference.md", REFERENCE_MD.format(**fills), force))
    results.append(write_file(root / "data" / "seeds" / ".gitkeep", "", force))

    # ── scripts/ ──
    results.append(write_file(root / "scripts" / "run.py", RUN_PY.format(**fills), force))
    results.append(write_file(root / "scripts" / "validate.py", VALIDATE_PY.format(**fills), force))
    results.append(write_file(root / "scripts" / "benchmark.py", BENCHMARK_PY.format(**fills), force))

    # ── errors/ ──
    results.append(write_file(root / "errors" / "error_codes.json", ERROR_CODES_JSON.format(**fills), force))

    return results


def scaffold_minimal(slug: str, title: str, desc: str, author: str,
                     dest: Path, force: bool, date: str) -> list[str]:
    """Minimal scaffold: only SKILL.md + manifest.json + CHANGELOG.md + LICENSE."""
    root = dest / slug
    fills = dict(slug=slug, title=title, desc=desc.strip(),
                 author=author, date=date, year=date[:4])
    results: list[str] = []

    results.append(write_file(root / "SKILL.md", SKILL_MD.format(**fills), force))
    results.append(write_file(root / "manifest.json", MANIFEST_JSON.format(**fills), force))
    results.append(write_file(root / "CHANGELOG.md", CHANGELOG_MD.format(**fills), force))
    results.append(write_file(root / "LICENSE", LICENSE_TEXT.format(**fills), force))

    return results


def scaffold_legacy(slug: str, title: str, desc: str,
                    dest: Path, force: bool, date: str) -> list[str]:
    """Legacy 7-pillar scaffold for backward compatibility."""
    root = dest / slug
    fills = dict(slug=slug, title=title, desc=desc.strip(), date=date)
    results: list[str] = []

    results.append(write_file(root / "SKILL.md", LEGACY_SKILL_MD.format(**fills), force))
    results.append(write_file(root / "CHANGELOG.md", LEGACY_CHANGELOG_MD.format(**fills), force))
    results.append(write_file(root / "scripts" / "run.py", LEGACY_RUN_PY.format(**fills), force))
    results.append(write_file(root / "references" / "reference.md", LEGACY_REFERENCE_MD.format(**fills), force))
    results.append(write_file(root / "assets" / "templates" / "output.md", LEGACY_OUTPUT_TEMPLATE_MD.format(**fills), force))
    results.append(write_file(root / "evals" / "evals.json", legacy_evals_json(slug), force))

    return results


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold a new skill with the Gold Standard (Altın Standart) structure.")
    parser.add_argument("name", help="Skill name (kebab-cased automatically).")
    parser.add_argument("--description", "-d", default="",
                        help="One-line intent; expanded into a pushy description in SKILL.md.")
    parser.add_argument("--author", "-a", default="Hermes Agent",
                        help="Author name for LICENSE and manifest.")
    parser.add_argument("--dest", default=DEFAULT_DEST,
                        help=f"Where to create the skill (default: {DEFAULT_DEST}).")
    parser.add_argument("--force", action="store_true",
                        help="Overwrite an existing skill directory. OFF by default.")
    parser.add_argument("--minimal", action="store_true",
                        help="SKILL.md + manifest.json + CHANGELOG + LICENSE only.")
    parser.add_argument("--legacy", action="store_true",
                        help="Old 7-pillar format (v1.x backward compat).")
    parser.add_argument("--date", default=None,
                        help="Override the CHANGELOG date (YYYY-MM-DD).")
    args = parser.parse_args(argv)

    try:
        slug = slugify(args.name)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    title = title_case(slug)
    desc = args.description or (
        f"[[FILL: one line on what the {slug} skill does and the outcome it produces.]]")
    date = _today(args.date)
    dest = Path(args.dest)

    if (dest / slug).exists() and not args.force:
        print(f"error: Skill directory already exists: {dest / slug}", file=sys.stderr)
        print("Refusing to overwrite. Re-run with --force to replace it.", file=sys.stderr)
        return 1

    try:
        if args.legacy:
            results = scaffold_legacy(slug, title, desc, dest, args.force, date)
            mode = "legacy 7-pillar"
        elif args.minimal:
            results = scaffold_minimal(slug, title, desc, args.author, dest, args.force, date)
            mode = "minimal"
        else:
            results = scaffold_gold(slug, title, desc, args.author, dest, args.force, date)
            mode = "Gold Standard (Altın Standart)"
    except FileExistsError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    for line in results:
        print(line)

    print(f"\n✅ Done. New {mode} skill scaffolded at: {dest / slug}")
    print("Next: replace every [[FILL: …]] placeholder in all files.")
    if not args.legacy:
        print(f"      Start with SKILL.md and manifest.json, then instructions/ and config/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())