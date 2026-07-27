# Writing a description that triggers reliably (pillar 1, deep dive)

> Read this when filling in a new skill's `description`. The description is the
> single biggest lever on whether a skill actually gets used. (Part of
> `skill-creator`; the automated tuning loop referenced at the end lives in this
> same skill.)

## How triggering works

Every skill shows up to Claude as **name + description** only. Claude picks which
skills to consult from those lines — the body isn't visible until after it
decides. Two consequences:

1. **The description must carry all the "when to use" information.** Don't stash
   trigger conditions in the body; the router never sees them in time.
2. **Simple one-step tasks may not trigger any skill**, because the model can
   just do them. Skills fire on substantive, multi-step, or specialized work.
   Write your triggers around tasks that genuinely benefit from the skill.

## The two-clause shape

```
<what it does, in one sentence> +
<the specific contexts, phrasings, and file types that should trigger it,
 phrased to lean into triggering>
```

Then optionally a third clause: a short negative boundary ("Do NOT use for … —
use <sibling> instead") so it doesn't over-fire.

## Be pushy (Claude under-triggers by default)

The current failure mode is skills *not* firing when they'd help. Counter it:

- Add "**Make sure to use this whenever…**" and "**even if the user doesn't say
  '<keyword>' explicitly**".
- List **many** real phrasings, not one canonical one. Formal, casual, abbreviated,
  typo'd. Include the user's languages — for Erman, Turkish **and** English terms
  side by side ("sözleşme özetle", "summarize this contract").
- Name the **file types and artifacts** that imply the skill (".docx", "kira
  sözleşmesi", "banka ekstresi").

## But bound it (so it doesn't become a magnet)

Pushiness without a boundary makes a skill grab near-misses. Balance every push
with a crisp negative clause that names the sibling that should win instead. This
is pillar 7 surfacing in the description, which is exactly right — the router
reads it here first.

## Worked before/after

> ❌ **Weak:** `Summarizes contracts.`
>
> ✅ **Strong:** `Summarizes Turkish and English contracts clause by clause and
> flags risky provisions. Make sure to use this whenever the user uploads or
> mentions a contract, agreement, "sözleşme", "kira kontratı", "gizlilik
> sözleşmesi", an NDA, or a .pdf/.docx that reads like a legal agreement — even
> if they just say "özetle" or "bunu bir bak". Do NOT use for drafting a brand-new
> contract from scratch (use the docx skill) or for binding legal/tax opinions
> (use vergi-hukuk-musaviri).`

Notice: what it does → many trigger phrasings in both languages → file types →
"even if they just say X" push → two negative boundaries with named siblings.

## Tuning it with data

Guesswork gets you a first draft; the automated loop gets you a good description.
Once the skill works, run the **description-optimization loop in this skill**
(`scripts/run_loop.py`, see the "Description Optimization" section of the main
SKILL.md): it generates should-trigger / should-not-trigger eval queries, measures
the real trigger rate (running each query several times), and proposes description
edits that raise the held-out score. Record the before/after trigger rate in the
CHANGELOG.
