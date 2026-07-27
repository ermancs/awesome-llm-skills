#!/usr/bin/env python3
"""workflow_scaffolder.py — emit a starter multi-agent workflow config (JSON).

Usage:
    python3 scripts/workflow_scaffolder.py <pattern> --name <name> [--output FILE]

Patterns: sequential | parallel | orchestrator | router | evaluator
If --output is omitted the JSON is printed to stdout. No third-party deps.
"""
import argparse, json, sys

def stage(role, prompt, **extra):
    s = {"role": role, "agent": role, "prompt": prompt,
         "handoff": "structured-json", "on_error": "retry-once-then-skip"}
    s.update(extra)
    return s

def scaffold(pattern, name):
    base = {"name": name, "pattern": pattern, "version": 1,
            "concurrency_cap": 8, "budget_tokens": None}
    if pattern == "sequential":
        base["stages"] = [
            stage("planner", "Decompose the task into ordered sub-steps."),
            stage("worker", "Execute each sub-step; pass results forward."),
            stage("verifier", "Check the output against the acceptance criteria."),
        ]
    elif pattern == "parallel":
        base["fanout"] = [stage(f"worker_{i}", f"Handle independent slice #{i}.")
                          for i in range(1, 4)]
        base["barrier"] = stage("synthesizer", "Merge all slices into one result.")
    elif pattern == "orchestrator":
        base["orchestrator"] = stage("orchestrator",
            "Receive the goal, dispatch specialist workers, integrate replies.")
        base["workers"] = [stage("specialist_a", "Own sub-domain A."),
                           stage("specialist_b", "Own sub-domain B.")]
    elif pattern == "router":
        base["router"] = stage("router", "Classify the request and pick one route.")
        base["routes"] = {"simple": stage("fast_path", "Answer directly."),
                          "complex": stage("deep_path", "Run the full pipeline.")}
    elif pattern == "evaluator":
        base["generator"] = stage("generator", "Produce a candidate answer.")
        base["evaluator"] = stage("evaluator",
            "Score the candidate; if below threshold, return feedback for a retry.",
            max_rounds=3, threshold=0.8)
    else:
        print(f"Unknown pattern: {pattern}", file=sys.stderr); sys.exit(2)
    return base

def main():
    ap = argparse.ArgumentParser(description="Scaffold a multi-agent workflow config.")
    ap.add_argument("pattern", choices=["sequential", "parallel", "orchestrator", "router", "evaluator"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--output")
    a = ap.parse_args()
    cfg = scaffold(a.pattern, a.name)
    text = json.dumps(cfg, indent=2, ensure_ascii=False)
    if a.output:
        import os
        os.makedirs(os.path.dirname(a.output) or ".", exist_ok=True)
        with open(a.output, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print(f"Wrote {a.output}")
    else:
        print(text)

if __name__ == "__main__":
    main()
