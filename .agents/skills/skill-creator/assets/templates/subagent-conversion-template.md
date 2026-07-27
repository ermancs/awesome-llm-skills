---
name: converting-legacy-subagents
description: Use this skill when migrating, transforming, or refactoring legacy Claude Code / Antigravity sub-agent definitions into modular, auto-triggering Agent Skills. Trigger whenever the user mentions "converting agents", "subagent to skill", or "agent refactoring".
license: MIT
metadata:
  author: enterprise-skill-architect
  version: "1.0.0"
---

# Sub-Agent to Skill Conversion Master Template

Standardized framework for refactoring legacy sub-agent configurations (`~/.claude/agents/` or `.claude/agents/`) into high-performance, auto-triggering Agent Skills.

## 🔄 Conversion Mapping Matrix

| Sub-Agent Component | Action Required | Converted Skill Equivalent |
| :--- | :--- | :--- |
| `name: code-reviewer` | Rename to gerund form | `name: reviewing-code-quality` |
| `description: Reviews code...` | Rephrase to pushy trigger | `description: Use this skill whenever reviewing code...` |
| `model: sonnet` | **Remove field** | Inherits full agent capabilities |
| `tools: [...]` | **Remove field** | Inherits full environment capabilities |
| Explicit `Task` invocation | Convert to auto-trigger | Invoked automatically by description matching |

## 📋 Step-by-Step Refactoring Workflow

### 1. Frontmatter Purification
Remove legacy fields (`model`, `color`, `tools`). Re-write description using the **Pushy Trigger Formula**:
> *"Use this skill whenever the user wants to [action]. Make sure to use this skill even if the user mentions [related keywords]."*

### 2. Name Standardization
Change noun-phrase names into gerund form:
- `debugger` → `debugging-runtime-errors`
- `data-extractor` → `extracting-structured-data`

### 3. File Re-organization & Progressive Disclosure
If legacy sub-agent prompt exceeds 300 lines:
- Extract detailed reference material into `./references/[intention-revealing-name].md`.
- Extract deterministic helper logic into `./scripts/[script-name].py` or `./scripts/[script-name].js`.

## 🧪 Conversion Verification Checklist

- [ ] `name` is lowercase, hyphens-only, gerund form, max 64 chars.
- [ ] `description` is trigger-focused, pushy, third-person, max 1024 chars.
- [ ] Frontmatter contains ONLY valid skill fields (`name`, `description`, `license`, `metadata`, `compatibility`).
- [ ] No residual legacy subagent parameters remain (`model`, `tools`, `color`).
- [ ] All supporting files use intention-revealing file names.
