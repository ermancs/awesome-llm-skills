# Gold Standard (Altın Standart) Skill Templates

These `*.tmpl` files mirror the scaffold that `scripts/new_skill.py` generates.
Use them **only when you can't run the Python generator** — the script is the
canonical source; these are kept in sync by hand.

## Structure (Gold Standard v2.0)

```
template/
├── SKILL.md.tmpl                     # Main agent file
├── manifest.json.tmpl                # Metadata & registry (REQUIRED)
├── README.md.tmpl                    # Human documentation
├── LICENSE.tmpl                      # MIT license
├── CHANGELOG.md.tmpl                 # Version history
├── instructions/
│   ├── system.md.tmpl                # System prompt
│   ├── constraints.md.tmpl           # Boundaries
│   └── style.md.tmpl                 # Output conventions
├── tools/
│   └── tool_1.json.tmpl              # Function schema
├── examples/
│   ├── basic/example_01.md.tmpl      # Basic usage
│   ├── edge_cases/missing_data.md.tmpl
│   └── conversational/example_01.md.tmpl
├── tests/
│   └── eval/evals.json.tmpl          # Eval prompts
├── config/
│   └── default.yaml.tmpl             # Runtime config + safety
├── src/
│   └── main.py.tmpl                  # Entry point
├── data/
│   ├── templates/output.md.tmpl      # Canonical output shape
│   └── knowledge/reference.md.tmpl   # Deep domain detail
├── scripts/
│   └── run.py.tmpl                   # Deterministic helper
└── errors/
    └── error_codes.json.tmpl         # Error catalog
```

## How to use manually

1. Copy this whole `template/` tree to your new skill's path.
2. Rename every `*.tmpl` file to drop the `.tmpl` suffix.
3. Replace the placeholders:
   - `{{NAME}}`  → the kebab-case skill name
   - `{{TITLE}}` → the human title
   - `{{DESC}}`  → a one-line intent
   - `{{DATE}}`  → today's date, `YYYY-MM-DD`
   - `{{AUTHOR}}` → author name
4. Then replace every `[[FILL: …]]` marker with real content.

## Quick validation

```bash
python /path/to/skill-creator/scripts/quick_validate.py <your-skill-dir>
```