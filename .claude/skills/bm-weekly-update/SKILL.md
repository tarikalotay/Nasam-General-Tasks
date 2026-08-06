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
8. **Create a ClickUp task for every action in Feedback from Call.** This is not
   optional and is the step most easily missed. For each bullet naming an owner:
   `clickup_create_task` into the list the action belongs to, assign the named person,
   set priority (`urgent` when the call said urgent), and put
   `From the WBR call, Wk NN (dd–dd Mon).` in the description. Then append the returned
   task id to that bullet on the page. A feedback bullet with no id has not been actioned.
   Bullets that are notes rather than actions ("out of scope", "no update") get no task.
9. **Name the page** `<Mon> - Wk <ISO week> (<dd>–<dd> <Mon>)`, e.g. `Jul - Wk 30 (20–26 Jul)`.
   Matches the existing convention (`Feb - Wk 8`, `Apr - Wk 17`).

## Counting rules

- The weekly metric is **Updated, not Done**. A task counts if it closed, changed
  status, or received a comment inside the window. Closure alone understates the work —
  most real progress here is logged as comments on tasks that stay open.
- **Count main tasks only.** Subtasks are excluded from every count. Pull them with
  `clickup_filter_tasks` + `subtasks: false` — that returns parent-level tasks directly,
  no tree walking needed. Say "Main tasks only. Subtasks are excluded from all counts."
  under the Overview.
- Subtasks still inform the *narrative* — ads levers, onboarding phases and barcode
  batches are where the work shows — they just do not inflate the numbers.
- Where a main task's only activity is on its subtasks, the main task counts as
  updated (e.g. the Inivita ads parent, worked entirely through its levers).
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

## Weekly sales — Brand x Channel

The sales week is **Thursday to Wednesday**, not the Mon–Sun task window. Compare it to
the Thu–Wed week immediately before.

```
mcp__Nasam__compare_sales_periods
  p1Start/p1End = the review Thu–Wed
  p2Start/p2End = the Thu–Wed before it
```

The response is ~64k characters and will overflow the tool limit — it lands in a file.
Parse it, do not read it:

- `p1.revenueSharePerBrandPerChannel` / `p2...` — array of
  `{brandName, saleChannel, trends:[{date, revenue, orders}]}`. Sum `trends[].revenue`
  per `(brandName, saleChannel)` for the week figure. **This is the Brand x Channel grain.**
- `growth.perBrand` and `growth.perSaleChannel` — ready-made p1/p2/`revenueGrowth` totals.
- `p1.totalRevenue` / `p2.totalRevenue` for the header line.

Report `Brand | Channel | This wk | Last wk | Chg`, sorted by this-week revenue. Drop
rows where both weeks are under 1 SAR. Mark a channel that went from zero as `new`, not
`+inf%`. Read the sales against the ads levers — a bid change and a revenue move on the
same brand/channel is the story worth putting on the page.

## Onboarding is tracked separately

**Onboarding is excluded from every count.** Its ~250 template subtasks and handful of
parents swamp the numbers and move for reasons that have nothing to do with the week's
work. State the exclusion under the Overview.

It gets its own section instead: a **narrative of at most 300 words total**, one short
paragraph per account, written the way a BM would say it out loud —

> Nokush: GS1 barcode closed, listings started on Amazon/Noon/Trendyol, list price
> confirmed but profitability still needs review with Massoud.

Name what closed, what started, what is blocked and on whom. Cover every account,
including any brand that has appeared in Brand Health but has no onboarding task yet —
that gap is itself the finding.

## Page structure

0. **Last Week's Actions** — every task raised at the previous call with its current
   status, closed ones first. Matches the LW/CW action-item convention the doc used
   before. Check whether closed tasks were actually done by the named owner; a task
   completed by someone else is worth a line.
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
3. **One section per function, matching the ClickUp lists** — Operations, Catalog &
   Pricing, Advertising, Brand Health, Store Enhancement. This is the canonical
   structure. Brands appear as rows inside each function's table, not as sections.
   Onboarding is its own narrative section and stays out of the counts.
4. **The structure does not change week to week.** A lead reading two consecutive pages
   must find the same sections in the same order. Wk 30 was per-list, Wk 31 was
   per-brand, and the inconsistency was the first thing raised. If a structural change
   is genuinely warranted, agree it on a call and change it once — never drift into it.
5. **By BM** — rollup table, bullets inside the cells.
6. **Escalations** — numbered table: Item · Owner · Status.

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

**No human-authored page in this doc uses tables at all.** Apr Wk 17 and every page
before it are plain lines plus pasted images. Markdown tables published through the API
become fixed equal-width column blocks that do not adapt to their content, and they
read back from `clickup_get_document_pages` as a single space — so **table rendering
cannot be verified through the API.** Never claim a table fits; you cannot see it.
Prefer plain lines for anything that is not genuinely a grid. Keep tables for the
sales WoW figures, where the columns really are numeric and comparable.

- **Cap at 4 columns.** 5 only when every cell is short. The Overview drops the Owners
  column entirely — owner splits live in the By BM table, and duplicating them made the
  Overview the widest table on the page.
- **Cap any cell at ~40 characters.** This is the rule that actually matters — column
  count is a proxy. A 4-column table with a 100-character cell is still unreadable.
- **Fold at most one `·` per cell.** Two or more clauses joined by `·` means the row
  should have been two rows. Fold count columns into one status cell
  (`7 running · 3 paused · 10 closed off`) rather than a column each.
- **One fact per row.** If a cell needs three clauses joined by `·`, split it into
  extra rows sharing the same Brand/Owner instead of widening the cell. Repeating
  `Nokush | Mohammed` down four rows is correct — it is not redundancy, it is the fix.
- **Metrics tables read `Channel | Lever | Result`.** Never put the setup and the
  outcome in one cell; the setup is the lever, the number is the result.
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

- **2026-08-06** — **Structure is per function, matching the lists — and it is fixed.**
  This supersedes the per-brand view trialled in Wk 31. Brands are rows inside each
  function's table. Changing structure between weeks was raised as a problem in its own
  right: consistency beats any single week's layout.
- **2026-08-06** — Sales tables carry an explicit **Growth** column, plus **by-brand** and
  **by-channel** rollups with their own growth rates, not just brand x channel rows.
- **2026-08-06** — Onboarding is **excluded from counts** and carries a **300-word max
  narrative per account** instead.
- **2026-08-06** — Page opens with **Last Week's Actions** — status of every task raised
  at the previous call.
- **2026-08-06** — **Cross-check sales against connection health.** Wk 31 showed Salla
  −89% across every brand; `sync_and_connection_health` showed no Salla channel
  connected for Marah and Brand Health had opened 4 new Salla fulfilment alerts. A
  channel-wide collapse is a connection failure until proven otherwise — never report it
  as demand.
- **2026-08-06** — **The accessible brand list can change between weeks.** Sondos was in
  the Wk 30 figures and gone in Wk 31, which silently rebases every total. Compare the
  brand list week to week and say plainly when totals are not comparable to the prior page.
- **2026-07-30** — Feedback bullets carry the **bare task id only**. Mentions are
  impossible through the API — `/mention`, `#`, `@` and the task URL were all tested on
  the live page and none produced one. Settled; do not retry.
- **2026-07-30** — `clickup_update_document_page` can return a transient 500. Retry once
  before reporting a failure; the retry succeeded.
- **2026-07-30** — Sales come from `compare_sales_periods` on a **Thu–Wed** week vs the
  prior Thu–Wed, at Brand x Channel grain via `revenueSharePerBrandPerChannel`.
- **2026-07-30** — The page moves to a **per-brand view** from Wk 31.
- **2026-07-30** — **Create a ClickUp task for every feedback action and write the id
  onto the page.** Missed entirely in Wk 30 and asked for directly.
- **2026-07-30** — Table rendering **cannot be verified through the API** — tables read
  back as a single space. Two "fixed" claims were made without evidence; do not make a
  third.
- **2026-07-29** — A main task counts as **updated when only its subtasks moved**
  (confirmed for the Inivita ads parent, worked entirely through its levers).
- **2026-07-29** — Width is governed by **cell length (~40 chars), not column count**.
  First pass passed the column rule and was still unreadable — 105-char cells.
- **2026-07-29** — Counts are **main tasks only** (`subtasks: false`), replacing the
  earlier tasks+subtasks rule. Totals drop ~489 → 98 and stop being dominated by
  onboarding and ads template scaffolding.
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
