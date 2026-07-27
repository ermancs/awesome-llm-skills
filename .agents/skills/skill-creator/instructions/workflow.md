# Eval / Test / Benchmark Workflow

> Extracted from SKILL.md to keep it lean. Read this when running test cases on a skill.

## Overview

This is one continuous sequence — don't stop partway through. Do NOT use `/skill-test` or any other testing skill.

Put results in `<skill-name>-workspace/` as a sibling to the skill directory. Within the workspace, organize results by iteration (`iteration-1/`, `iteration-2/`, etc.) and within that, each test case gets a directory with a descriptive name.

## Step 1: Spawn all runs (with-skill AND baseline) in the same turn

For each test case, spawn two subagents in the same turn — one with the skill, one without.

**With-skill run:**
```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <eval files if any, or "none">
- Save outputs to: <workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/
- Outputs to save: <what the user cares about — e.g., "the .docx file", "the final CSV">
```

**Baseline run:**
- **Creating a new skill**: no skill at all. Same prompt, no skill path, save to `without_skill/outputs/`.
- **Improving an existing skill**: snapshot the old version first (`cp -r <skill-path> <workspace>/skill-snapshot/`), then point baseline at the snapshot. Save to `old_skill/outputs/`.

Write an `eval_metadata.json` for each test case (assertions can be empty for now). Give each eval a descriptive name.

## Step 2: While runs are in progress, draft assertions

Draft quantitative assertions for each test case and explain them to the user.

Good assertions are objectively verifiable and have descriptive names. Subjective skills (writing style, design quality) are better evaluated qualitatively.

Update `eval_metadata.json` files and `tests/eval/evals.json` with the assertions once drafted.

## Step 3: As runs complete, capture timing data

When each subagent task completes, save `total_tokens` and `duration_ms` immediately to `timing.json` in the run directory:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

This is the only opportunity to capture this data — it comes through the task notification.

## Step 4: Grade, aggregate, and launch the viewer

1. **Grade each run** — spawn a grader subagent that reads `agents/grader.md`. Save results to `grading.json`. The expectations array must use fields `text`, `passed`, and `evidence`. For assertions that can be checked programmatically, write a script — faster, more reliable, reusable.

2. **Aggregate into benchmark:**
   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
   ```
   Produces `benchmark.json` and `benchmark.md`.

3. **Do an analyst pass** — see `agents/analyzer.md`. Look for non-discriminating assertions, high-variance evals, time/token tradeoffs.

4. **Launch the viewer:**
   ```bash
   nohup python <skill-creator-path>/eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "my-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json \
     > /dev/null 2>&1 &
   ```
   For iteration 2+, also pass `--previous-workspace <workspace>/iteration-<N-1>`.
   
   **Cowork / headless**: use `--static <output_path>` to write a standalone HTML file.

5. **Tell the user**: "I've opened the results in your browser. 'Outputs' tab for test cases, 'Benchmark' tab for quantitative comparison."

## What the user sees in the viewer

- **Outputs tab**: Prompt, output files (rendered inline), previous output (collapsed), formal grades, feedback textbox
- **Benchmark tab**: Pass rates, timing, token usage per config, per-eval breakdowns
- Navigation: prev/next buttons or arrow keys. "Submit All Reviews" saves to `feedback.json`.

## Step 5: Read the feedback

When the user is done, read `feedback.json`:

```json
{
  "reviews": [
    {"run_id": "eval-0-with_skill", "feedback": "the chart is missing axis labels", "timestamp": "..."},
    {"run_id": "eval-1-with_skill", "feedback": "", "timestamp": "..."}
  ],
  "status": "complete"
}
```

Empty feedback = user thought it was fine. Focus improvements where there's specific complaint.

Kill the viewer: `kill $VIEWER_PID 2>/dev/null`