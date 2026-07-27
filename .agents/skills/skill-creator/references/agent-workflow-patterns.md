# Layer 1 — AI Multi-Agent Workflow Patterns

Reference catalog of production multi-agent workflow patterns. Each entry: when to use,
handoff contract, and the main failure mode to guard against. Pair with
`scripts/workflow_scaffolder.py` to emit a starter config.

## 1. Sequential (pipeline)
- **Use when** the task is a fixed chain: each step needs the prior step's output.
- **Handoff:** structured JSON between stages; later stages reference earlier
  results by field, not by re-deriving them.
- **Failure mode:** one slow/failed stage blocks the chain. Mitigate with
  per-stage `retry-once-then-skip` and a clear acceptance check at the end.

## 2. Parallel (fan-out / barrier)
- **Use when** independent slices can run concurrently and must be merged.
- **Handoff:** all workers return the same schema; a synthesizer merges them.
- **Failure mode:** the barrier wastes the fast workers' time if one is slow, and
  a partial failure can silently drop a slice — always `filter(Boolean)` results.
- **Failure policy (declare one explicitly):**
  - `fail_fast` — abort the whole group on the first worker error (use when any
    missing slice invalidates the merge).
  - `continue_on_error` — keep the successful slices, drop the failed ones, and
    record what was dropped (use when partial coverage is still useful).
  - `all_or_nothing` — commit results only if every worker succeeds, else discard
    the batch (use when downstream needs a complete, consistent set).

## 3. Orchestrator–workers
- **Use when** a coordinator must decompose, dispatch to specialists, and integrate.
- **Handoff:** orchestrator owns state; workers are stateless and bounded.
- **Failure mode:** orchestrator context bloat. Keep worker outputs small and
  summarize before integrating.

## 4. Router (dispatch)
- **Use when** requests fall into distinct classes with different cost/depth.
- **Handoff:** a classifier picks exactly one route; routes don't overlap.
- **Failure mode:** misclassification. Add a default/fallback route and log the
  chosen route for audit.

## 5. Evaluator–optimizer (generate → judge → retry)
- **Use when** quality matters more than latency and output can be scored.
- **Handoff:** generator produces a candidate; evaluator returns score + feedback;
  loop until threshold or max rounds.
- **Failure mode:** infinite/expensive loops. Cap `max_rounds` and require the
  evaluator to justify a score ≥ threshold before accepting.

## 6. Human-in-the-loop gate (approval step)
- **Use when** an action is outward-facing or hard to reverse (send, publish,
  deploy, spend) and a human must approve before the flow continues.
- **Handoff:** the gate receives a compact decision packet — proposed action, its
  inputs, and a short rationale — and returns `approved | rejected | edited`.
  On `edited`, the human's revised payload replaces the proposed one downstream.
- **Design as a first-class step,** not a bolt-on: the topology pauses at the gate
  and resumes (or halts) on the decision, so approval is auditable and resumable.
- **Failure mode:** silent auto-approval when no human responds. Default to *hold*
  (never auto-proceed) and log the pending decision; pair with a timeout/escalation.

## Cross-cutting controls
- **Context budget:** cap concurrency; summarize between stages.
- **Determinism:** prefer code-driven control flow (loops/conditionals) over
  model-driven dispatch where the structure is known in advance. When the
  topology is fixed, declare it (e.g. a YAML routing graph with explicit
  conditions) so the structure is diffable, version-controlled, and reviewable
  before any run. Deterministic routing also consumes no model tokens — an
  evaluator–optimizer loop can iterate many times with zero routing overhead.
- **Cost:** scale fan-out to the task; log any silent truncation (top-N, sampling).
- **Safety gates:** put validation/T&S checks as explicit stages, not afterthoughts.

> Choose the simplest pattern that fits. A single well-scoped prompt beats an
> unnecessary workflow; reach for these only when one prompt is insufficient.

---
*Pattern enrichments (named parallel failure policies, human-in-the-loop gate,
declarative/zero-token deterministic routing) adapted from concepts in Microsoft
Conductor (MIT-licensed, github.com/microsoft/conductor). Concepts only — no
source text reproduced.*
