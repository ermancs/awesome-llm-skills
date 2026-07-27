# Interactive Requirement Discovery & Spec Refinement Framework

Framework for conducting structured user interviews to extract hidden domain rules, edge cases, and business logic before creating a skill.

## 🎙️ 4-Phase Interactive Interview Protocol

### Phase 1: High-Level Intent & Trigger Scope
- **Goal**: Define what the skill does and what phrases should invoke it.
- **Key Questions**:
  1. *"What primary outcome or deliverable should this skill produce?"*
  2. *"What user queries or file types should trigger this skill automatically?"*

### Phase 2: Domain Rules & Edge Case Probing (The Deep Probe)
- **Goal**: Uncover domain-specific nuances, exclusions, and business logic.
- **Domain Specific Probes**:
  - **Financial / Cash Flow**: *"Are there internal transfers (repos, virman, inter-account transfers) that must be excluded from cash flow? Are cash outflows different from accounting costs?"*
  - **Data Processing**: *"How should missing fields, malformed CSVs, or unexpected data types be handled?"*
  - **Code Generation**: *"What architectural patterns, linting rules, or framework versions are required?"*

### Phase 3: Input/Output Contract & Deterministic Rules
- **Goal**: Lock down exact inputs, expected outputs, and calculations.
- **Key Questions**:
  1. *"What is the exact structure of input files?"*
  2. *"What is the exact target schema or markdown structure of the output?"*
  3. *"Are there calculations that require exact code/scripts rather than LLM inference?"*

### Phase 4: Spec Synthesis & Sign-Off (`skill-spec.md`)
- **Goal**: Synthesize all answers into a clean `skill-spec.md` artifact.
- Present `skill-spec.md` to the user for confirmation before writing any skill files.

---

## 📄 `skill-spec.md` Artifact Schema

```markdown
# Skill Specification: [skill-name]

## 1. Trigger & Scope Definition
- **Target Gerund Name**: `[verb-ing-name]`
- **Pushy Description**: `[Trigger-focused description]`
- **Included Scenarios**: `[...]`
- **Excluded Scenarios**: `[...]`

## 2. Business Rules & Domain Logic
- **Rule 1 (Exclusions)**: `[...]`
- **Rule 2 (Calculations)**: `[...]`

## 3. Input & Output Contract
- **Input Format**: `[...]`
- **Output Schema**: `[...]`

## 4. Required Deterministic Scripts
- `scripts/[script-name].py`: `[Purpose]`

## 5. Verification Matrix
- Test Prompts: `[...]`
- Assertions: `[...]`
```
