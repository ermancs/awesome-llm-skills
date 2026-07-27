---
name: analyzing-example-workflow
description: Use this skill whenever the user wants to process, analyze, or transform data files, perform automated workflow validation, or generate structured reports. Make sure to trigger this skill even if the user asks generally about "data processing", "report generation", or "checking file quality".
license: MIT
metadata:
  author: enterprise-skill-architect
  version: "1.0.0"
---

# Enterprise Skill Architecture Template

Comprehensive, deterministic workflow template for high-reliability agent operations.

## 🎯 Core Purpose & Scope

- **Primary Goal**: Provide deterministic, reproducible execution for [Target Domain].
- **Key Deliverables**: Validated outputs, structured artifacts, and clear summary execution logs.

## 🟢 When to Use

- When the user explicitly requests: `"[Trigger Keyword 1]"`, `"[Trigger Keyword 2]"`.
- When processing input files of format: `.json`, `.csv`, `.md`.
- When complex multi-step analysis or data transformation is required.

## 🔴 When NOT to Use

- Do NOT use for simple single-line status queries.
- Do NOT use when external non-granted API endpoints are required without permission.

## 📋 Deterministic Step-by-Step Workflow

### Step 1: Input & Environment Audit
- Inspect target directory or input files.
- Verify required local binaries or libraries are available.

### Step 2: Core Processing & Transformation
- Execute main processing logic or invoke bundled scripts in `scripts/`.
- Apply strict data validation rules.

### Step 3: Artifact Generation & Output Verification
- Write resulting outputs to the designated target directory.
- Verify file non-emptiness and schema compliance.

## 🛡️ Error Handling & Edge Cases

| Failure Scenario | Root Cause | Recovery / Fallback Action |
| :--- | :--- | :--- |
| Missing Input File | File path invalid or deleted | Prompt user with exact missing path |
| Schema Validation Error | Malformed JSON/CSV structure | Log specific line error and halt safely |
| Dependency Missing | Tool not installed | Provide one-click install command |

## 📚 Supporting References & Progressive Disclosure

- Load `./references/domain-rules.md` for complete domain specifications.
- Execute `./scripts/validate-schema.py` for automated file auditing.

## ✅ Quality Checklist

- [ ] Frontmatter `name` uses gerund form (`verb + -ing`).
- [ ] `description` includes pushy trigger phrases to prevent undertriggering.
- [ ] SKILL.md body remains under 500 lines.
- [ ] All supporting files use intention-revealing file names.
