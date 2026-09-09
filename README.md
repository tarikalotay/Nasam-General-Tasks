# Nasam-General-Tasks

General Nasam working repo. Currently home to the versioned **Nasam Claude skills**.

## Claude skills

The account-level Nasam skills (`sdlc`, `ux-discovery`, `ux-touch`, `clickup`) live in
[`.claude/skills/`](.claude/skills/) — see [that README](.claude/skills/README.md) for how they are
kept in sync with upstream and how to set them up locally.

Because they are committed here, Claude Code also loads them automatically when working in this repo.

```bash
.claude/skills/scripts/check-skills.sh   # validate before committing or uploading
```

> ⚠️ **This repository is public.** No credentials, no internal IDs. `check-skills.sh` enforces both.
