# Description Optimization

> Extracted from SKILL.md. Read this after the skill is functionally complete to optimize triggering.

The description field in SKILL.md frontmatter is the primary mechanism that determines whether Hermes invokes a skill. After creating or improving a skill, offer to optimize the description for better triggering accuracy.

## Step 1: Generate trigger eval queries

Create 20 eval queries — a mix of should-trigger and should-not-trigger:

```json
[
  {"query": "the user prompt", "should_trigger": true},
  {"query": "another prompt", "should_trigger": false}
]
```

Queries must be **realistic** — concrete, specific, with file paths, personal context, company names. Bad: `"Format this data"`. Good: `"ok so my boss just sent me this xlsx file (its in my downloads, called something like 'Q4 sales final FINAL v2.xlsx') and she wants me to add a column..."`

**Should-trigger (8-10):** Different phrasings of the same intent. Some formal, some casual. Include cases where the user doesn't explicitly name the skill but clearly needs it.

**Should-not-trigger (8-10):** Near-misses — queries that share keywords but need something different. Don't make them obviously irrelevant ("Write a fibonacci function") — the negative cases should be genuinely tricky.

## Step 2: Review with user

1. Read the template from `assets/eval_review.html`
2. Replace placeholders: `__EVAL_DATA_PLACEHOLDER__`, `__SKILL_NAME_PLACEHOLDER__`, `__SKILL_DESCRIPTION_PLACEHOLDER__`
3. Write to `/tmp/eval_review_<skill-name>.html` and open it
4. User edits queries, toggles should-trigger, clicks "Export Eval Set"
5. File downloads to `~/Downloads/eval_set.json`

## Step 3: Run the optimization loop

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id-powering-this-session> \
  --max-iterations 5 \
  --verbose
```

Splits 60% train / 40% test, runs each query 3 times, iterates up to 5 times. Returns `best_description` selected by test score (not train) to avoid overfitting.

## How skill triggering works

Hermes only consults skills for tasks it can't easily handle on its own. Simple one-step queries like "read this PDF" may not trigger a skill even if the description matches perfectly. Complex, multi-step, or specialized queries reliably trigger skills. Your eval queries should be substantive enough that Hermes would actually benefit from consulting a skill.

## Step 4: Apply the result

Take `best_description` from the JSON output and update the skill's SKILL.md frontmatter. Show before/after and report the scores.