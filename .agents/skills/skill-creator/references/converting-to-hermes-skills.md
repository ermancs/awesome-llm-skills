---
name: converting-to-hermes-skills
description: "Detailed guide for converting Claude Code sub-agents, other platform skills, and CLI workflows into Hermes Agent skill format."
---

# Converting Claude Code Sub-Agents to Hermes Skills

This document provides detailed guidance on converting existing Claude Code sub-agent configurations to the Hermes Agent Skills format.

## Understanding the Differences

### Sub-Agent Configuration (Claude Code)

Sub-agents are defined in files (in `~/.claude/agents/` or `.claude/agents/`) with YAML frontmatter:

```yaml
---
name: agent-name
description: What this agent does (for Task tool invocation)
tools: [optional tool restrictions]
model: sonnet|opus|haiku
---

Agent instructions and expertise...
```

**Key characteristics:**
- Invoked explicitly by main Claude instance via Task tool
- Operate in separate context windows
- Description explains what the agent does (for explicit selection)
- Model and tools can be specified
- Self-contained instructions

**Example from Documentation — Code Reviewer:**
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

### Skill Configuration (Hermes Agent)

Skills are directories with a `SKILL.md` file:

```yaml
---
name: skill-name
description: "Use when [trigger situation] — [one-line behavior]."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [descriptive, tags]
    related_skills: [related-skill]
---

Skill instructions and expertise...
```

**Key characteristics:**
- Invoked automatically by Hermes when relevant (no explicit Task tool needed)
- Description must trigger invocation (keywords + use cases)
- Starts with "Use when ..." (not "Use this skill when ...")
- Includes version, author, license, tags, related_skills metadata
- No model/tools specification (inherits all Hermes capabilities)
- Can have supporting files (templates, scripts, references)
- Uses progressive disclosure

## Key Transformation Steps

### 1. Description Transformation (MOST CRITICAL)

Sub-agent descriptions explain WHAT the agent does. Skill descriptions must explain WHEN to invoke.

**Transformation Formula:**
```
Sub-Agent: "Reviews code quality and provides feedback"
Skill:     "Use when reviewing code for quality issues, security vulnerabilities, performance problems, or best practices violations. This includes analyzing pull requests, auditing existing code, or validating new implementations."
```

**Guidelines:**
- Write in third person
- Start with "Use when ..."
- Include specific trigger keywords users might say
- List concrete use cases
- Keep under 1024 characters
- Think: "What user queries should invoke this?"

### 2. Name Transformation

**Sub-Agent Names** (typically nouns or noun-phrases):
- `code-reviewer`
- `debugger`
- `csv-helper`

**Hermes Skill Names** (lowercase-hyphens, max 64 chars):
- No gerund requirement (unlike Claude Code skills)
- Can keep the original name if it's already lowercase-hyphens
- Prefer action-oriented names
- `code-reviewer` → keep as `code-reviewer` or `reviewing-code`
- `debugger` → keep as `debugger` or `debugging-applications`
- `csv-helper` → `analyzing-csv-data` or `csv-processing`

### 3. Metadata Transformation

**Add Hermes metadata fields:**
- `version: 1.0.0`
- `author: Hermes Agent`
- `license: MIT`
- `metadata.hermes.tags: [relevant, tags]`
- `metadata.hermes.related_skills: []`

**Remove:**
- `model` field (not applicable to Hermes skills)
- `tools` field (sub-agent tool restrictions)
- `allowed-tools` field (skills inherit all capabilities)

### 4. Tool Reference Adaptation

| Claude Code | Hermes Agent |
|-------------|-------------|
| `WebFetch` | `web_extract` / `web_search` |
| `claude -p "..."` | `execute_code(code)` or `terminal(command)` |
| Node.js scripts | Python scripts (via execute_code) |
| `~/.claude/skills/` | `~/.hermes/skills/` or `skill_manage(action='create')` |
| `.claude/skills/` (project) | `skills/<category>/<name>/` (in-repo) |
| `allowed-tools` field | Remove entirely |
| Sub-agent `model` field | Remove entirely |
| Sub-agent `tools` field | Remove entirely |

### 5. Path Adaptation

- Replace `~/.claude/skills/` with `~/.hermes/skills/`
- Replace `~/.claude/agents/` with `~/.hermes/skills/` (skills replace sub-agents)
- For in-repo skills: replace `.claude/skills/` with `skills/<category>/`

### 6. Scripting Adaptation

- Replace Node.js ESM examples with Python equivalents
- Both Python and Node.js are acceptable, but Python is preferred for new scripts
- Use `execute_code` for Python, `terminal` for shell commands

### 7. Enhance with Progressive Disclosure

- Add references/ directory for detailed content
- Add templates/ directory for output patterns
- Add scripts/ directory for reusable Python utilities
- Keep SKILL.md focused on core workflow

## Complete Conversion Example: Code Reviewer

**Original Sub-Agent Configuration:**
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

Review the code and provide clear, actionable feedback.

## Process

1. **Read the code** — Use `read_file` or `search_files` to understand the full context
2. **Analyze each area** — Check quality, security, performance, and practices
3. **Prioritize findings** — Critical > Major > Minor > Suggestion
4. **Provide feedback** — Clear, actionable, with specific line references and fix suggestions
```

## Quick Reference

| Aspect | Sub-Agent | Hermes Skill |
|--------|-----------|-------------|
| Invocation | Explicit (Task tool) | Automatic (description match) |
| Location | `~/.claude/agents/` | `~/.hermes/skills/` |
| Description focus | WHAT it does | WHEN to invoke |
| Model field | Required | Remove |
| Tools field | Optional | Remove |
| Scripts | Node.js | Python (preferred) |
| Supporting files | No | Yes (references/, templates/, scripts/) |