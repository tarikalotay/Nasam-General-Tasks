---
name: bm-weekly-update
description: Build the weekly Brand Manager (BM) update for the Nasam Brands Management workspace in ClickUp and publish it as a new page in the BM WBR doc. Use when asked for the BM weekly update, WBR page, brand manager progress, "what did the team achieve this week", per-BM achievements, or open callouts/escalations from ClickUp. Tracks team progress week over week.
---

# BM Weekly Update (ClickUp → BM WBR)

Produce a sharp, low-text weekly review of Brand Manager activity and publish it as a
new page in the **BM WBR** doc. The reader is a lead who will run a call off it — the
page carries the facts, the BM explains the detail verbally.

## Goal

Track team progress weekly: what each BM achieved, what is pending, and what needs
escalation. Structure is **by list first**, brand second, BM third.

## Fixed IDs

| Thing | ID |
| --- | --- |
| Workspace | `90181204512` |
| Space — Brands Management | `90184521046` |
| **BM WBR doc** (publish here) | `2kzkfyh0-4958` |
| WBR Guidelines page | `2kzkfyh0-4398` |

Lists in the Brands Management space:

| List | ID |
| --- | --- |
| Onboarding | `901819321555` |
| Catalog and Pricing | `901819315575` |
| Operations | `901819314962` |
| Brand Health by System | `901818876425` |
| Advertising and Promotions | `901819315782` |
| Store Enhancement and Marketing | `901818869414` |

Team member IDs (for `assignees` filters):

| Person | ID |
| --- | --- |
| Khaled Alashgr | `95587428` |
| Mohammed Alrowitea | `107585711` |
| Rashed Alotay | `95597807` |
| Fahad Alhssan | `95585689` |
| Ibrahim Alothman | `95585691` |
| Tarik Alotay | `194571442` |
| Salman Alkhalifah | `107631936` |
| Mohamed Eladawy | `107631935` |

## Process

1. **Set the window.** Monday–Sunday of the review week. Convert to epoch ms and keep
   the bounds — every "done" claim must be checked against them.
2. **Pull each list** with `clickup_filter_tasks` (`list_ids`, `include_closed: true`).
   Page size caps at 100; page until empty.
3. **Pull comments** on every task that changed in the window. The comment text *is*
   the update — status alone is not an update.
4. **Resolve the tree.** For any parent with unassigned subtasks, use
   `clickup_get_task` with `include: ["subtasks"]` and walk down until leaves.
5. **Classify** each item: done-in-window / open / blocked / no-activity.
6. **Write the page** using the structure below and publish with
   `clickup_create_document_page` into doc `2kzkfyh0-4958`.
7. **Name the page** `<Mon> - Wk <ISO week> (<dd>–<dd> <Mon>)`, e.g. `Jul - Wk 30 (20–26 Jul)`.
   Matches the existing convention (`Feb - Wk 8`, `Apr - Wk 17`).

## Counting rules

- Counts include **tasks + subtasks**.
- An unassigned subtask counts under **its parent's assignee**.
- A shared parent counts for **every** assignee — so owner figures do not sum to the
  list total. State this once under the table; never silently reconcile it.
- "Done" means `date_closed` **inside the window**, or a comment confirming completion
  inside the window. Items closed days before the window are not this week's work.
- Report owner counts as `Name (done/total)`, covering **assigned items only**.

### Overview owners column

- Comma-separated names with `(done/total)` appended: `Ibrahim (0/21), Khaled (0/63)`.
- Keep the **same names in the same order** week to week. Do not reorder by volume —
  a stable column is easier to read across weeks.
- Do **not** add "Unassigned" as an owner. Unassigned work sits outside the column;
  cover the gap in the footnote instead.
- Someone active on a list but holding no assigned tasks is marked `Name (reviewer)`,
  not `(0/0)`.
- Footnote under the table must state that owner figures do not sum to the list total,
  and name the gap (shared tasks counted twice, unassigned closures excluded).

## Page structure

1. **Overview** — one row per list: Total · Done · Open · Owners (done/total) · Update.
2. **One section per list**, heaviest/most material first. Each gets a one-line summary
   plus a brand-level table.
3. **By BM** — rollup table, bullets inside the cells.
4. **Escalations** — numbered table: Item · Owner · Status.

For Advertising and Promotions use the brand view: `Brand | Type | Channel — update`,
with channels as bullets inside the third cell.

See `references/page-template.md` for the full skeleton.

## Style

- **No editorial commentary.** No "strongest week", no praise, no emoji verdicts.
  Facts and numbers only. ✅/⚠️ as status markers is fine.
- **Low text.** If a BM's section runs long, cut it — they explain on the call.
- **If there is no update, write "No update"** in bold. Never pad it, never infer
  progress from a status field that nobody commented on.
- Brand level, not task level. Collapse many tasks into one brand row.
- Include the channel (Amazon / Noon / Trendyol / Salla / Jahez …) wherever known.

## Pitfalls

These have each produced a wrong report. Check every one.

- **Ads updates live on the lever subtasks, not the brand parent.** Each brand parent
  in Advertising and Promotions has ~20 lever subtasks (PPC, Coupon, Deals, Discount,
  Sponsor Brand …). The parent's comments are empty. Reading only parents produces a
  false "no advertising reporting" — it has happened. Always open the subtasks.
- **Chat channels are empty.** Every channel in the space has zero messages. Tracking
  is via task comments. Do not report chat activity as a gap each week; just use tasks.
- **Onboarding is a deep template tree** (~255 items, 4 levels). Walk it with
  `include: ["subtasks"]`. Its counts are approximate — label them so.
- **Onboarding template subtasks are scaffolding**, not weekly load. Keep the count
  visible but do not let it imply workload.
- **Brand Health tasks are auto-generated** by the Nasam system and may show `complete`
  with a null `date_closed`. Read the comments for `Recovered to Healthy on YYYY-MM-DD`.
  Watch for recover→re-escalate cycles; flag when a recovery does not hold.
- **Check `date_closed` against the window every time.** Items closed a day or two
  before the window look done and are not.
- **Verify parent vs subtask before splitting counts** — `clickup_get_task` returns a
  `parent` field. Do not guess from names.
- **`clickup_update_document_page` can fail with a ClickUp server error** and leave the
  page untouched. It is not always transient-looking — always re-read the page with
  `clickup_get_document_pages` to confirm the write landed, then retry.
- **When asked to change one column, change only that column.** Re-read the current
  page first and diff against it — do not rebuild the table from memory and quietly
  reorder rows, drop names, or reword the footnote.

## Changelog

Keep this current — the skill is expected to grow.

- **2026-07-29** — Overview owners column rules (stable order, no "Unassigned",
  `(reviewer)` for non-assignees, required footnote). Added pitfalls: verify the doc
  write landed; change only the column asked for.
- **2026-07-29** — Created. By-list structure, brand-level ads view, owner done/total
  figures, subtask rollup rule, pitfalls from the Wk 30 build.
