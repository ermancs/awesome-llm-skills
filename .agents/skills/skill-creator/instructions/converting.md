# Converting Sub-Agents to Hermes Skills

> Extracted from SKILL.md. Read when converting Claude Code sub-agents or other platform skills.

## Quick Overview

1. **Analyze** the sub-agent's YAML frontmatter and instructions
2. **Transform description** — change from "Reviews code" to "Use when reviewing code"
3. **Convert to Hermes format** — remove `model`, `tools`, `color`; add `version`, `author`, `license`, `metadata.hermes`
4. **Replace tool references** — WebFetch → web_extract, claude -p → execute_code, Node.js → Python, ~/.claude/ → ~/.hermes/
5. **Enhance with progressive disclosure** and supporting files
6. **Create** via `skill_manage(action='create')` or `write_file`

## Key Differences at a Glance

| Aspect | Claude Code Sub-Agent | Hermes Skill |
|--------|----------------------|--------------|
| Invocation | Explicit (Task tool) | Automatic (description match) |
| Location | `~/.claude/agents/` | `~/.hermes/skills/` |
| Description focus | WHAT it does | WHEN to invoke |
| Model field | Required | Remove |
| Tools field | Optional | Remove |
| Scripts | Node.js | Python (preferred) |
| Supporting files | Optional | Gold Standard: 10 directories |
| Frontmatter | name + description + model + tools | name + description + version + author + license + metadata |

## Complete Conversion Example: Code Reviewer

**Original Sub-Agent:**
```yaml
---
name: code-reviewer
description: Reviews code quality, checks security and best practices, provides prioritized feedback
model: sonnet
---

You are an expert code reviewer focusing on:
- Code quality and maintainability
- Security vulnerabilities
- Performance issues
- Best practices adherence

Review the code and provide clear, actionable feedback.
```

**Converted Hermes Skill:**
```yaml
---
name: code-reviewer
description: "Use when reviewing code for quality issues, security vulnerabilities, performance problems, or best practices violations. This includes analyzing pull requests, auditing existing code, or validating new implementations."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [code-review, security, quality, best-practices]
    related_skills: []
---

# Code Reviewer

You are an expert code reviewer focusing on:
- Code quality and maintainability
- Security vulnerabilities
- Performance issues
- Best practices adherence

## Process

1. **Read the code** — Use `read_file` or `search_files` to understand the full context
2. **Analyze each area** — Check quality, security, performance, and practices
3. **Prioritize findings** — Critical > Major > Minor > Suggestion
4. **Provide feedback** — Clear, actionable, with specific line references and fix suggestions
```

For comprehensive guidance, see `references/converting-to-hermes-skills.md`.