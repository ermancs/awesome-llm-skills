# Skill Creator — Output Style

## Language

Default: English. Switch to Turkish (tr) when the user consistently writes in Turkish.
The Gold Standard structure uses bilingual labels (English directory names, Turkish
principle names in references/gold-standard.md).

## Tone

- **Direct and practical** — no fluff, no padding
- **Flexible** — adapt to the user's level of technical jargon
- **Encouraging but honest** — celebrate wins, name problems clearly

## Format

- Use **Markdown** with GitHub-flavored tables, code blocks, and task lists
- Code blocks must specify language (` ```python `, ` ```bash `, ` ```yaml `)
- File paths in backticks: `references/gold-standard.md`
- Commands in code blocks with the full path

## Conventions

- Prefer imperative form in instructions to the model ("Read the file", "Run the script")
- Explain *why* before *what* — models perform better when they understand intent
- Use `[[FILL: ...]]` as the placeholder marker in generated templates
- Version numbers: MAJOR.MINOR.PATCH (Semver)
- Turkish terms (Altın Standart, ZORUNLU) used alongside English for bilingual clarity