# Nasam Claude skills

The Nasam-specific Claude skills, versioned. These are the four that live at the **account level**
(synced to claude.ai and available in every session, in any repo) — as opposed to the repo skills in
`Nasam-co/nasam/.claude/skills/` and `nasam-frontend-v2/.claude/skills/`, which only load inside
those checkouts.

| Skill                            | What it does                                                        |
| -------------------------------- | ------------------------------------------------------------------- |
| [`sdlc`](sdlc/)                   | Full fullstack feature lifecycle across the two repos, gate by gate |
| [`ux-discovery`](ux-discovery/)   | Deep UX/product discovery before a feature is built                 |
| [`ux-touch`](ux-touch/)           | Small, targeted UX addition to an already-shipped feature           |
| [`clickup`](clickup/)             | Create and manage ClickUp tasks for project tracking                |

Supporting, not skills:

- `_shared/nasam-business-context.md` — the canonical product/user context (see below)
- `scripts/` — sync and validation

## Why the business context is generated

`ux-discovery` and `ux-touch` both need the product and user context inline. Account skills upload to
claude.ai as **self-contained bundles**, so one skill cannot read another's files — the context has to
be physically present in each `SKILL.md`.

Hand-maintaining two copies is what caused the drift this repo was created to fix: `ux-touch`'s copy
had lost the **Growth Consultants** user entirely and disagreed with `ux-discovery` on how many brands
an AM handles. So the context now lives once in `_shared/nasam-business-context.md` and is **injected**
into each skill between marker comments.

Edit the source, never the injected block:

```bash
$EDITOR .claude/skills/_shared/nasam-business-context.md
.claude/skills/scripts/sync-shared.sh      # regenerate the blocks
.claude/skills/scripts/check-skills.sh     # verify
```

`check-skills.sh` fails if a block was edited by hand, so drift cannot come back silently.

## Keeping up with upstream

Fahad is the primary author; these skills change often. This repo is a **downstream copy**, not the
source of truth for skill *content* — it is where the shared context, the secret hygiene, and the
validation live.

To take an update:

1. Pull the new `SKILL.md` from wherever Fahad published it (account sync, or the repo skills).
2. Diff it against the copy here — **`git diff` is the review**, and it is the point of this repo.
3. Re-apply the local invariants if the incoming version dropped them:
   - no credentials in files (`CLICKUP_TOKEN` comes from the environment)
   - no hardcoded `/Users/<someone>/…` paths
   - shared context stays inside the markers
4. Run `./scripts/check-skills.sh` — it enforces all of the above.
5. Commit with what changed upstream and what you re-applied.

To push a change **up**, edit here, run the checks, then upload the skill folder to claude.ai
(Settings → Capabilities → Skills) so the account copy matches.

## Local setup

`clickup` needs two things that are deliberately not in git:

```bash
export CLICKUP_TOKEN="pk_..."   # your own personal token, not a shared one
cp .claude/skills/clickup/references/clickup-ids.{example,local}.md
$EDITOR .claude/skills/clickup/references/clickup-ids.local.md
```

## Validation

```bash
.claude/skills/scripts/check-skills.sh
```

Checks frontmatter (`name` present and matching the directory, `description` present), credential-shaped
strings, hardcoded home directories, and shared-context drift. Run it before every commit and before
uploading a skill.
