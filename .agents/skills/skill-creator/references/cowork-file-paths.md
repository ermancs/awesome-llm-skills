# Cowork: file paths, registration, matching & folder states

Read this when creating, editing, packaging, or troubleshooting why a skill
"doesn't show up" in Cowork. These facts were verified against a live Cowork
session, not assumed.

## 1. Where skills actually live (paths)

| What you see | What it is |
|--------------|------------|
| `/mnt/user-config/.claude/skills/{name}/` | The skills root **inside the container** — a FUSE mount that is *supposed* to sync to OneDrive. You write here. **But do not assume a write reaches OneDrive immediately** — see §2; this has been observed to lag or diverge within a session. |
| OneDrive Graph path: `/Belgeler/Cowork/skills/{name}/` | The cloud copy. **Verified exact path** (via Graph). Subtlety: the user's personal drive's display name is itself `Belgeler` (Turkish for "Documents", webUrl `.../Documents`), AND there is a folder *literally named* `Belgeler` inside the drive root. So from the drive root the path is `/Belgeler/Cowork/skills/...` — **not** `/Cowork/skills/...` (that 404s). The `Cowork` folder may have been renamed/moved by the user; capitalization `skills` vs `Skills` has both been seen. |
| `/Users/<user>/Library/CloudStorage/OneDrive-<tenant>/Belgeler/Cowork/skills/` | The user's **Mac local** view of that same OneDrive folder. You cannot read this local path from the container. |
| `/opt/workspace-config/.claude/skills/` | **Built-in system skills. Read-only.** Never write here. |

How to reach the cloud copy with the OneDrive tools:
- Get the drive id with `GetDefaultDrive` (returns e.g. `drive_1`). The well-known
  alias `@user-onedrive` does **not** always resolve — prefer the real id.
- Then `GetDriveChildren(drive_id="drive_1", item_path="/Belgeler/Cowork/skills/...")`
  or `SearchDrive` to inspect cloud state.

Also note **two distinct index files**: `…/Cowork/skills-index.md` (one level
*above* `skills/`) is separate from `…/Cowork/skills/skills-index.md` (the one
`build_index.py` writes via the mount). Don't confuse them.

Correction to an earlier overstatement: the mount is the *intended* sync source,
but it is **not** guaranteed to be byte-identical to OneDrive at any instant.
Treat "written to the mount" and "present in OneDrive" as two separate facts and
**verify the cloud side with Graph** (above) when it matters.

## 2. Write-back timing — and a real divergence to watch for

Nominal path from your edit to the user's other devices:

```
write to FUSE mount  →  rclone flush (~5s)  →  blob replication to OneDrive (~30s)
```

So a change *usually* appears in OneDrive within ~35s, and a brand-new skill
becomes triggerable only in the **next session** (the available-skills list loads
at session start, see §4).

**Verified failure mode (do not gloss over this):** in at least one session the
mount held the new files (correct content + size on disk) while OneDrive still
showed the *old* state — the writes had not propagated up, and an unrelated
edit even produced a `… (conflicted …).md` copy in the cloud. The sync can also
pull cloud→container and overwrite an in-flight edit ("revert").

Consequences for how you should behave:
- After an important write, **verify on the cloud side with Graph** (§1), not just
  by re-reading the mount. The mount agreeing with itself proves nothing about
  OneDrive.
- If the cloud is stale, say so honestly. You **cannot** force-push a file to
  OneDrive from here: there is no upload tool, and `CallGraph` only sends JSON
  bodies, so `PUT …/content` cannot carry raw file bytes. The reliable
  user-visible deliverable is a **packaged `.skill` in `output/`** (the output
  channel syncs), which the user can re-install.
- Re-applying the write and re-checking the on-disk timestamp is still worth
  doing, but frame the mount as "queued to sync", not "already in OneDrive".

## 3. Registration: the central catalog (`skills-index.md`)

At the skills root there is `skills-index.md` — a flat catalog the agent reads at
the start of each session (progressive disclosure). It is maintained by the
`beceri-index` skill, **not** auto-generated on every change, so it goes stale.

Symptom: a skill exists on disk and validates, but "doesn't show up" in the
user's inventory/catalog view. Cause: it was added to disk after the catalog was
last built, so it was never listed. (Older skills still appear, which is why the
gap is confusing.)

Fix — rebuild the catalog from the actual `SKILL.md` files (source of truth):

```bash
python3 ../beceri-index/scripts/build_index.py --write-index
```

This scans every directory under the skills root, parses each `SKILL.md`
frontmatter (`name`, `description`, `active`), tags which resource dirs exist
(`scripts`, `references`), and overwrites `skills-index.md` with an accurate
count. Skills with `active: false` in frontmatter are listed as passive/bypassed.

After adding or renaming any skill, rerun this so the catalog stays in sync.

## 4. Matching: how triggering actually works

Two different surfaces, often confused:

- **Live trigger list (skill picker / `available_skills`)** — built at session
  start from each skill's `name` + `description`. A skill edited or created
  mid-session is **not** picked up until the next session. The `description`
  field is the entire triggering mechanism; keep it specific and slightly
  "pushy" to combat under-triggering.
- **Catalog (`skills-index.md`)** — the inventory the agent reads; independent of
  the live picker. A skill can be in the live picker but missing from the
  catalog (the staleness case in §3), or vice-versa right after a rebuild before
  a new session starts.

So "X gözükmüyor / X doesn't show up" has two distinct fixes: rebuild the catalog
(§3) for the inventory view, and wait for the next session for the live picker.

## 5. Folder states you will encounter

- **A valid skill** = a directory containing `SKILL.md`. Optional resource dirs:
  `scripts/`, `references/`, `assets/`, `agents/`, `data/`, `imported/`.
- **`*-workspace/` and `*-main/` siblings** — scratch/eval output or import
  staging from other skills. They usually have **no `SKILL.md`**, so the catalog
  generator skips them. Don't treat them as skills.
- **`.skill` files at the skills root** — leftover packaged artifacts (zips) from
  a prior `package_skill` run. Harmless, but clean up ones you created so they
  don't clutter the folder.
- **`__pycache__/`** — Python bytecode caches. `package_skill.py` already excludes
  them from `.skill` archives; no need to commit or ship them.
- **`.claude-plugin/*.plugin.json`** — optional plugin bundles that group several
  skills with routing rules. A skill does **not** need to be in a plugin to work;
  these are for deconflicting related skills, not registration.

## 6. Quick troubleshooting checklist

1. Does `{name}/SKILL.md` exist and validate? `python3 scripts/quick_validate.py {name}`
2. Is it in `skills-index.md`? If not, rebuild the catalog (§3).
3. Did the edit happen this session? The live picker needs a new session (§4).
4. Frontmatter clean? Only `name, description, license, allowed-tools, metadata,
   compatibility` are allowed at top level; put anything else (e.g. `status`,
   `cowork`) under `metadata:`. No angle brackets (`<`, `>`) in `description` —
   use `{placeholder}` instead.
5. Did a sync revert it? Re-check the on-disk timestamp (§2) and re-apply if lost.
