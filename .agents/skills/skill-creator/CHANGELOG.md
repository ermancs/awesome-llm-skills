# Changelog

Notable changes to the **skill-creator** skill.
Format: [Keep a Changelog](https://keepachangelog.com/); versioning: SemVer.

## [Unreleased] — 2026-07-04

### Fixed (Cowork uyumu — denetim sonrası)
- **Yanlış Cowork iddiası düzeltildi:** "Description optimization should work in Cowork just
  fine" iddiası gerçekle hizalandı — `run_loop.py`/`run_eval.py`/`improve_description.py`
  `claude -p` CLI'ye bağımlı ve bu CLI Cowork konteynerinde yok; ayrıca `run_eval.py` Claude Code
  `.claude/commands/` proje düzeni varsayıyor. Artık Cowork'te elle/alt-ajanla yapılması söyleniyor.
- **Masaüstü-özel komutlar Cowork'e uyarlandı:** `open /tmp/...eval_review.html` → `output/`'a
  statik HTML + link; `~/Downloads/eval_set.json` → Cowork'te kullanıcıdan yeniden ekleme.
- **Description Optimization bölümüne baştan bir Cowork uyarı bloğu** eklendi.
- Guardrail'daki `ANTHROPIC_API_KEY` notu netleştirildi (optimizer session auth kullanır, ayrı key gerekmez).
- Kalite skoru 98 → **98** korundu (skor kapılı, regresyon yok).

### Added
- **Multi-sub-agent authoring capability**, absorbed from `is-akisi-muhendisligi`
  (workflow engineering), which is now superseded and removed. skill-creator can
  now author skills that orchestrate several sub-agents, not just single-prompt
  or linear ones.
- New SKILL.md section "Authoring multi-agent skills (the multi-sub-agent
  orchestration archetype)" — the six core topologies (sequential, parallel,
  router, orchestrator-workers, evaluator-optimizer, human-in-the-loop), the
  scaffolder workflow, handoff contracts, and the cross-cutting controls
  (determinism, idempotency, timeouts/budget, observability).
- `scripts/workflow_scaffolder.py` — emits a starter multi-agent workflow config
  (sequential / parallel / orchestrator / router / evaluator); standard library
  only, carried over unchanged from `is-akisi-muhendisligi`.
- `references/agent-workflow-patterns.md`, `references/durable-execution-temporal.md`,
  and `references/automation-platforms.md` — Layer 1/2/3 depth references,
  transferred from `is-akisi-muhendisligi`.
- Description extended to cover multi-agent authoring + folded-in workflow
  triggers (multi-agent skill, "iş akışı / workflow tasarla", orchestration), and
  the "Do NOT use" clause now redirects application-code work to
  `kidemli-yazilim-muhendisi` and MCP-server work to `mcp-builder`.

### Rationale
- The user asked to transfer `is-akisi-muhendisligi`'s capabilities into
  skill-creator (making it able to write multiple sub-agents) and then delete the
  standalone skill. Workflow/orchestration design is a natural extension of
  authoring: a skill's operating instructions can *be* a multi-agent workflow, so
  the knowledge belongs where skills are built. `orkestra-sefi`'s delegation was
  redirected from `is-akisi-muhendisligi` to `skill-creator`, and
  `skills-index.md` was updated.

## [Unreleased] — 2026-07-03

### Added
- **7-pillar fast-path scaffold.** New `scripts/new_skill.py` deterministically
  generates a complete skill skeleton with all seven pillars pre-wired (pushy
  description, progressive disclosure, deterministic script, CHANGELOG, eval,
  templates, scope guard) and `[[FILL: …]]` markers on every human-decision spot.
  Runs on the Python standard library (no network install).
- `references/seven-pillars.md` — full rationale + a worked example per pillar.
- `references/description-guide.md` — how to write a description that triggers
  reliably without over-firing.
- `assets/skill-template/` — copyable `*.tmpl` version of the 7-pillar tree for
  when Python can't be run.
- A "Fast path: scaffold the 7 pillars deterministically" subsection in SKILL.md,
  under "Anatomy of a Skill".

### Rationale
- Folded in what briefly existed as a standalone `skill-scaffold` skill. Keeping
  it separate would have collided with skill-creator's own "create a skill"
  triggers (mis-routing) and added a 51st always-loaded description for no gain.
  Scaffolding is the first step of authoring, so it belongs here.
