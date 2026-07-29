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
5. **Classify** each item: updated-in-window / open / blocked / no-activity.
6. **Write the page** using the structure below and publish with
   `clickup_create_document_page` into doc `2kzkfyh0-4958`.
7. **Check escalation responses.** Re-read the tasks behind each escalation and state
   whether any response was logged. "No response logged" is itself a finding worth
   stating at the top of the Escalations table.
8. **Name the page** `<Mon> - Wk <ISO week> (<dd>–<dd> <Mon>)`, e.g. `Jul - Wk 30 (20–26 Jul)`.
   Matches the existing convention (`Feb - Wk 8`, `Apr - Wk 17`).

## Counting rules

- The weekly metric is **Updated, not Done**. A task counts if it closed, changed
  status, or received a comment inside the window. Closure alone understates the work —
  most real progress here is logged as comments on tasks that stay open.
- Counts include **tasks + subtasks**.
- An unassigned subtask counts under **its parent's assignee**.
- A shared parent counts for **every** assignee — so owner figures do not sum to the
  list total. State this once under the table; never silently reconcile it.
- Check every timestamp against the window. Items closed or commented a day or two
  before it look current and are not.
- Report owner counts as `Name (updated/total)`, covering **assigned items only**.
- **A closed parent implies its subtasks are closed.** Do not report subtasks of a
  closed parent as "not started" — check the parent's status first and say
  "parent still in progress" only when that is actually true.

### Overview owners column

- Names with `(updated/total)` appended, separated by ` · `: `Ibrahim 8/21 · Khaled 0/42`.
- Keep the **same names in the same order** week to week. Do not reorder by volume —
  a stable column is easier to read across weeks.
- Do **not** add "Unassigned" as an owner. Unassigned work sits outside the column;
  cover the gap in the footnote instead.
- Someone active on a list but holding no assigned tasks is marked `Name (reviewer)`,
  not `(0/0)`.
- Footnote under the table must state that owner figures do not sum to the list total,
  and name the gap (shared tasks counted twice, unassigned closures excluded).

## Page structure

1. **Feedback from Call** — **always the first section on the page**, above Overview.
   A **flat bullet list**, not tables. One bullet per point, `**Owner** — action.`
   Keep it to the main points; no sub-bullets, no grouping headers.
   Publish it with only the heading and an italic prompt line — **no empty bullets**,
   which ClickUp renders as the literal text `null.`
   **Record only what the team said.** Never list your own report changes in it
   (formatting decisions, metric redefinitions, section moves) — those are not
   feedback and do not belong on the page. Apply them silently and mention them in
   chat instead.
   **Once the lead has written in it, never delete or replace their text.** Tighten
   wording, fix an owner or a date — but the content is theirs. If the section reads
   as empty, say so and ask; do not infer what was decided.
2. **Overview** — one row per list: Total · Updated · No update · Owners (updated/total).
   Owners goes **last** — it is the longest column and must wrap at the page edge.
3. **One section per list**, heaviest/most material first. Each gets a one-line summary
   plus a brand-level table.
4. **By BM** — rollup table, bullets inside the cells.
5. **Escalations** — numbered table: Item · Owner · Status.

Advertising and Promotions takes two tables: a brand summary
(`Brand | Owner | Lever status | Update`) and, for each brand actually being worked, a
detail table (`Type | Channel | Update`) with **one row per channel**.

See `references/page-template.md` for the full skeleton.

## Style

- **No editorial commentary.** No "strongest week", no praise, no emoji verdicts.
  Facts and numbers only. ✅/⚠️ as status markers is fine.
- **Low text.** If a BM's section runs long, cut it — they explain on the call.
- **If there is no update, write "No update"** in bold. Never pad it, never infer
  progress from a status field that nobody commented on.
- Brand level, not task level. Collapse many tasks into one brand row.
- Include the channel (Amazon / Noon / Trendyol / Salla / Jahez …) wherever known.

### Tables must fit the container

ClickUp does not scroll tables horizontally — a wide table is unreadable on the call.

- **Cap at 5–6 columns.** Fold count columns into one status cell
  (`7 running · 3 paused · 10 closed off`) rather than a column each.
- **One fact per row.** If a cell needs three clauses joined by `·`, split it into
  extra rows sharing the same Brand/Owner instead of widening the cell.
- **Give each channel its own row.** Never stack `<br>`-separated channel bullets in a
  single cell — that was the widest cell on the page. `Type | Channel | Update` reads
  cleanly and stays narrow.
- **Put the longest column last** so it wraps at the page edge (e.g. Owners in Overview,
  after Update).
- Shorten list names in table cells: `Advertising`, `Brand Health`, `Catalog & Pricing`.
- Use first names only in the By BM table.
- Drop restating figures that appear elsewhere on the page.

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
- **Re-pull immediately before the call.** The workspace changes during the review day.
  On Wk 30 a whole brand tree (Nokush ads, 21 items) was created and another brand was
  reassigned to a different BM within an hour of publishing. Re-run the list pulls and
  correct Overview totals, owner figures and the By BM table before the call starts.
- **Ad lever subtasks roll up to the brand parent's assignee in the By BM totals**, the
  same as any other unassigned subtask. Missing this understates the ad owners by ~20
  each and makes the Overview and By BM tables disagree.
- **Never infer the channel from a task name.** Ads levers repeat the same names
  (`PPC Weekly Update` appears three times under one brand, one per channel). The
  channel is the **`Sales Channel` custom field** — fetch it with
  `include: ["custom_fields"]` and read the dropdown index against `type_config.options`
  (0 Amazon 3P · 1 Amazon Retail · 2 Trendyol · 3 Noon · 4 Ninja · 5 Jahez · 6 Salla ·
  7 Zid · 8 The Chefz · 9 Hungerstation · 10 Keeta). Guessing from names put figures
  against the wrong marketplace in a page the whole team reads. Same field carries
  `📋 Brand` and `Promo Type`.
- **BMs post results after the window closes**, often on the day of the review, and
  they edit existing comments in place rather than adding new ones. Re-pull comments on
  every active item right before the call. Label anything outside the window with its
  date (`Result (29 Jul)`) — never fold it into the week's counts.

## Changelog

Keep this current — the skill is expected to grow.

- **2026-07-29** — Feedback from Call is a flat bullet list, not tables, and carries
  only what the team said — never the assistant's own report changes.
- **2026-07-29** — Wk 30 call: Feedback from Call moved to the top of the page; metric
  redefined from Done to Updated; closed parent implies closed subtasks; check and
  state escalation responses every week.
- **2026-07-29** — Tables must fit the container (cap columns, one fact per row, one
  row per channel, longest column last). Feedback from Call uses empty table rows, not
  bullet stubs, which ClickUp renders as `null.` Lead's written feedback is never
  deleted — adjust only.

- **2026-07-29** — Pitfall: read the channel from the `Sales Channel` custom field,
  never from the task name. This page is read by the whole team — wrong-channel
  figures are the most damaging error the report can make.
- **2026-07-29** — Pitfall: BMs post results after the window and edit comments in
  place; re-pull before the call and date-label post-window figures.
- **2026-07-29** — Overview owners column rules (stable order, no "Unassigned",
  `(reviewer)` for non-assignees, required footnote). Added pitfalls: verify the doc
  write landed; change only the column asked for.
- **2026-07-29** — Created. By-list structure, brand-level ads view, owner done/total
  figures, subtask rollup rule, pitfalls from the Wk 30 build.
