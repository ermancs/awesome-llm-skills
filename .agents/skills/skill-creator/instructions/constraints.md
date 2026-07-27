# Skill Creator — Constraints

## Absolute Constraints

- **Never fabricate benchmark results** — if a subagent fails, report the failure
- **Never skip the eval viewer generation** in testing workflows — get results in front of the human before self-evaluating
- **Never overwrite an existing skill without --force confirmation**
- **Never create skills that contain malware, exploits, or unauthorized access mechanisms**

## Data Boundaries

- **Max skill name length**: 64 characters (kebab-case)
- **Max description length**: 1024 characters
- **Max SKILL.md size**: ~500 lines recommended; offload detail to instructions/ or references/
- **Max subagents per test batch**: 3 (delegation.max_concurrent_children)

## Cost Limits

- **Max cost per skill creation session**: 10.0 USD
- **Max iterations in description optimization**: 5

## Network

- **Allow network**: false (scaffolding and validation are local-only)
- **Allow file write**: true (skills are written to ~/.hermes/skills/)

## Blocked Paths

- `/etc`, `/sys`, `~/.ssh`