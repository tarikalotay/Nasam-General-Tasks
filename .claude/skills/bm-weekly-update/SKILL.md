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
| Nasser Abuwandah | `308593216` |

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
   **Re-test the underlying condition, not just the comment thread.** A connection or
   sync alert must be checked against `sync_and_connection_health` before it is carried
   forward. Wk 40 found `86eyu8uwx` still _update required_ after five weeks while every
   Sonbol and Invita stream — Salla and Trendyol settlements included — read
   **Connected · Healthy**. The alert was stale, not open. **Carrying a resolved alert as
   an escalation is as wrong as missing a real one**, and it costs the lead call time on
   something that only needs closing.
8. **Create a ClickUp task for every action in Feedback from Call.** This is not
   optional and is the step most easily missed. For each bullet naming an owner:
   `clickup_create_task` into the list the action belongs to, assign the named person,
   set priority (`urgent` when the call said urgent), and put
   `From the WBR call, Wk NN (dd–dd Mon).` in the description. Then append the returned
   task id to that bullet on the page. A feedback bullet with no id has not been actioned.
   Bullets that are notes rather than actions ("out of scope", "no update") get no task.
   **Search the target list for an existing task first.** A recurring call item usually
   already has a task from a prior week — comment on that one and re-date it rather than
   creating a second. Wk 31 created "Upload the Ninja POs" when "Upload the Ninja PO to
   the system" had been open since Wk 30; both had to be closed later as duplicates.
9. **Name the page** `<Mon> - Wk <ISO week> (<dd>–<dd> <Mon>)`, e.g. `Jul - Wk 30 (20–26 Jul)`.
   Matches the existing convention (`Feb - Wk 8`, `Apr - Wk 17`).

## Check the workspace shape before counting

Lists and tasks move between weeks. Diff against the prior page before trusting any
count, and say on the page when the shape changed — a list that shrinks because tasks
moved is not progress.

Seen so far: the **Store Enhancement list was emptied into Advertising** (Wk 33), the
**QC registrations moved from Operations into Onboarding**, The Chefz registration was
deleted, and tasks were renamed (`Onboarding Plan (Shared With Sonbol)` →
`(Shared With Dar Sonbol)`).

**Lists get renamed and disappear too.** By Wk 40 `Brand Health by System` returns from
the API as just **`Brand Health`**, and `Store Enhancement and Marketing` no longer
appears in the space at all. Match list sections on the **list id**, never the name, and
keep the page's heading stable even when ClickUp's label changes — the reader is
comparing weeks, not reading ClickUp.

**New task ids no longer all start `86ey`.** The two alerts opened on 2 Oct came back as
`z8xxqw7bhj` / `z8xxqw7bhh`. Never filter or sort task ids on a prefix.

**A new AM rebases every count in one week.** Nasser Abuwandah added **16 main tasks**
across Catalog, Operations and Advertising in Wk 42 — Catalog went 10 → 17 — and closed
five of them. Never report list growth as backlog growth without naming who created it,
and never read a new joiner's open cards as the team's deteriorating throughput. Check
too whether their new card **duplicates an existing one**: the Sondos purchase-order
problem landed on Khaled's 44-day `pending clent` card and on Nasser's fresh card in the
same week, with the new one carrying the actual cause. Say they need merging rather than
counting the work twice.

**Work migrates to the wrong list.** Sonbol/Tenda's effective onboarding — Amazon brand
registry, A+ content, size charts, the summer collection — ran entirely through Catalog
and Pricing while the Onboarding list showed nothing. Report where the work actually is,
and say that the list which should own it is silent.

**A brand rename in flight breaks every week-over-week figure.** Sonbol is mid-rename to
**Tenda** (`z8xxqwaf6v`, run with Okasha on the main account). Flag a rename the week you
see it, ask for the cutover date, and expect the brand to appear under both names in the
sales data across the changeover.

**Watch for wholesale assignee changes.** In Wk 34 Mohammed Alrowitea vanished as
assignee from all ~50 of his tasks in one move, with the work transferred to Tarik. The
per-AM tables would otherwise have shown this as one person's heroic week and another's
disappearance. When a name drops out of the workspace entirely, lead with it — it is a
staffing event, not a productivity result — and never present the receiving person's
inherited backlog as their own throughput.

**The accessible brand list also changes.** Sondos vanished in Wk 31 and returned in
Wk 33; Graffiti Resin and Sonbol appeared in Brand Health with no onboarding task behind
them. A brand appearing in Brand Health but absent from Onboarding is a finding worth
stating.

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
- **`date_updated` is not evidence that an AM updated anything.** Phase 0's own nudge
  comments bump it on every stale task, so a list can look busy in the metadata and be
  completely silent. When deciding "updated", discount comments from the service account
  beginning `⏰ WBR Phase 0`, ClickBot's `@assignees` line at creation, and the system's
  own `Recovered to Healthy` / `Escalated to Needs action` notes. In Wk 40, 24 tasks
  carried a `date_updated` inside or after the window and **not one had a human comment
  in it** — the whole week's movement was Phase 0 and two auto-generated alerts.
- **Bound the comment pull by `date_updated`.** A comment bumps `date_updated`, so a task
  whose `date_updated` predates the window cannot hold in-window activity. Pull comments
  only for tasks with `date_updated >= window start` — in Wk 40 that was 24 of 126 and
  made the comment check cheap. Include tasks updated *after* the window too; they may
  still carry an in-window comment under a later one.
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
`+inf%`.

**Prior-week figures restate downward — the `Last wk` column will not match the prior
page's `This wk`.** Re-querying 24–30 Sep a week later returned **12,907** against the
**13,795** published on the Wk 40 page: the same week, 6% lower, as returns and
cancellations netted off. Invita Amazon restated 4,988 → 4,521 and Sondos Trendyol
4,469 → 4,049. Marketplace revenue keeps settling for roughly a fortnight. **Always
compute both periods from the same single `compare_sales_periods` call** so the two
columns are internally consistent, then say on the page that the prior week has restated
and by how much. Never quietly reconcile to the published figure, and never present the
gap as an error.

**New channels appear in the data without warning.** Namshi (channel id 14) showed up in
Wk 41 carrying Sonbol's first marketplace revenue. Keep the **Total on Amazon · Noon ·
Trendyol** so it stays comparable with every prior page, and give a new channel its own
row **outside the Total**, flagged for a scope decision — the same treatment as Nokush's
Salla. Folding a channel into the Total mid-stream rebases every week-over-week number on
the page.

**Nokush's Salla is in scope and is no longer zero.** It ran 243 in Wk 39 and 140 in
Wk 40. Give it its own row, labelled `Salla — Nokush only`, and keep it **outside the
Total** so the headline marketplace figure stays comparable with every prior page.
AlFaris Group Salla stays excluded entirely.

**Separate a demand move from a basket move before writing a word about it.** Put
revenue growth next to order growth: Wk 42 fell **32% on orders down only 7%**, so
average basket went 116 → 85 SAR. That is fewer large orders, not fewer customers, and it
reads completely differently on the call. A drop with orders flat is pricing, promotion or
mix; a drop with orders down is demand or availability.

**A brand falling across every channel on a healthy connection is a stock or buyability
question before it is a demand question.** Wk 42's Invita −62% was an outright
**Amazon stock-out — every SKU 0 available, 450 units inbound** — found by checking live
stock, not by reading the task lists, where no card existed for it. Add
`inventory_live` to the cross-check beside `sync_and_connection_health`; it needs
**both `brand` and `channel`** (brand alone errors), so call it per channel on any brand
down more than ~40%. Where stock is present and revenue still fell, say so and name the
other candidate — Invita held 315 units on Noon and still fell 73%, which pointed at the
deal, not the shelf.

**Before calling a revenue jump real, apply three tests.** A 5x swing has twice been
settlement catch-up, so do not assume either way:
1. **Did orders move with it?** Wk 40 was +80% revenue on +62% orders — proportional, so
   trading. The 46–49k fortnight was flat orders on 5x revenue — settlement.
2. **Is it spread across the days?** Split the window by day at marketplace grain. A
   single huge day is a posting batch; a lift on every day is demand.
3. **Are settlements healthy?** `sync_and_connection_health` per brand, checking the
   `Settlements` stream's `lastSyncedAt`, not just `brandWide.state`.
Then ask whether it **fades inside the week**. Wk 40 ran 3,117 on Thursday down to 812 by
Wednesday — a holiday tail, not a new baseline. Say which it is; a lead who reads +80%
as the new level will plan against it. Read the sales against the ads levers — a bid change and a revenue move on the
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

Fixed order. Do not vary it week to week. A lead reading two consecutive pages must find
the same sections in the same order.

1. **Action Items — This Call** — empty, filled live during the call. Heading plus an
   italic prompt line only; no empty bullets (they render as the literal `null.`).
   Once the lead has written in it, never delete or reword their text.
   **If it is still empty 5 hours after the call, the feedback is delayed — say so in
   one line and stop.** Do not infer actions from the call, do not chase, do not ask
   again. The lead re-runs the capture step themselves once their notes are on the page.
2. **Last Week's Action Items** — every task raised at the previous call with its status.
   **Verify each against the task itself before writing "No update".** Read the comments,
   not just the status field. Wk 31 reported Khaled as silent when he had commented four
   times on Wadi Halfa. **Partial is its own status** — say which brand moved and which
   did not. Note when a task was closed by someone other than its named owner.
3. **Sales — Brand x Channel** — three tables: brand x channel, by brand, by channel.
   Every one carries an explicit **Growth** column.
4. **One section per list**, in this order: Catalog and Pricing · Operations ·
   Brand Health by System · Advertising and Promotions · Store Enhancement and Marketing.
   Each is headed by an open vs complete count — `**6 complete · 5 open** of 11`, adding
   `· N cancelled` where it applies — then a **per-AM table**:
   `AM | Done | Open | Overdue | Not completed`, with open task names as bullets inside
   the last cell (`<br>`-separated). **Overdue** = a due date in the past on a task that
   is not complete; it is the column that makes the table worth reading, so compute it.
   **Unassigned work gets its own row in EVERY per-AM table** — Brand Health and the
   Advertising matrix included, not just Operations and Catalog. Ad lever subtasks carry
   no assignee of their own and silently inherit the brand parent's; list them as
   unassigned rather than crediting them to the parent's owner.
   Follow the table with prose on the week's material activity.

   **Two lists take their own table shape:**

   - **Brand Health by System** — `AM | Done | Updated | No Update | Not completed
     (updated / not updated)`. Check last week's activity per alert and split the last
     cell into *Updated:* and *Not updated:* groups. An alert that is open and untouched
     is the finding; one that is open and being worked is not.
   - **Advertising and Promotions** — a **campaign-level matrix**, not counts:
     `AM | Active campaign with update | Active campaign, no update | Paused`.
     List the individual campaigns as bullets in each cell, formatted
     `Channel lever - Brand` (e.g. `Trendyol Deals - Sondos`, `Amazon PPC - Invita`).
     This means walking each brand's lever subtasks, not just the brand parent —
     `clickup_get_task` on the brand parent with `include: ["subtasks"]`, one call.
     **Since the 21 Sep rebuild the tree is three levels, not two:**
     `Brand → Ads / Promotions → one card per channel` (Amazon · Noon · Trendyol). One
     call on the brand parent returns only `Ads` and `Promotions`; the channel cards are
     a level below and are where an update would actually be written. Five brands means
     **30 channel cards**. A report that stops at the brand parent sees 5 pending cards
     and misses that 30 are untouched. The channel cards carry **no assignee of their
     own** — list them unassigned, and say that nobody is named on an individual channel.
     **Lever names in ClickUp do not carry the channel** — they are all
     "PPC Weekly Update", "Deals Weekly Update" etc., repeated once per channel batch.
     Read the `Sale Channel` custom field to label them; do not infer the channel from
     batch order without saying so. Invita ran 19 levers in Wk 31 — 8 running, 2 paused
     (Amazon Coupon, Meta Ads), 9 cannot-implement — against the "7 levers" figure
     carried on earlier pages, so count them rather than trusting the prior week.
     **A blank ad card may be a decision, not neglect — read the comments before calling
     it silence.** Wk 41's Nokush card carried "we are not going to spend any money on
     ads on all platforms until you update us": the spend was frozen group-wide pending
     the lead, which reframed four weeks of empty cards. Report a frozen account as
     frozen, then make the two real findings — the freeze is recorded on **one** card out
     of five, so a reader cannot tell frozen from abandoned, and "until you update us"
     carries no review date while the work it blocks has one.
5. **Onboarding** — no counts, activity narrative only. **Group by brand under its own
   `###` heading**, one short paragraph each, 300 words max total.
6. **Escalations** — numbered table: Item · Owner · Status.
7. **Update Quality** — up to 10 of the week's weakest task comments, so the team learns
   what a usable update contains. `Task · ID | AM | Update given | What is missing` —
   **four columns, never five**; ClickUp clips the fifth, which would drop the whole
   point of the section. Include "no comment at all" cases, and include your own updates
   when they are thin — the lead's Nokush clearance note was in the first one.

   **Judge every update against five questions:** scope (all selection or a chosen
   category, how many SKUs) · size (number, percentage, budget) · window (start and end
   date) · channel (which marketplace) · next (who does what, by when).

   > Weak: "Discount created on old stock."
   > Strong: "32% clearance on 14 legacy SKUs, Amazon and Noon, 15 Aug to 30 Sep,
   > target 80% sell-through before the new brand goes live."

   **An alert that closes on a system recovery is not the AM's answer landing.** Arabesque
   profitability auto-closed on "Recovered to Healthy on 2026-10-15" four days after
   Khaled answered a *margin* alert with a *stock* sentence. Credit the close to the
   recovery and still carry the update as weak — otherwise the page teaches that any
   sentence works as long as the metric drifts back on its own.

   **The commonest AM failure mode is a comment that says resolved on a card that stays
   open.** Four landed in one Sunday in Wk 41 — Sense buy box "already fixed" still
   `to do`, Arabesque inventory "all stock updated" still `update required`, both new
   profitability alerts answered and still `to do`. The board is what the WBR counts, so
   this reads as eight more weeks of open work. Name each one and say plainly that it
   needs closing or a reason.

   **Check for one answer pasted across several tasks.** In Wk 41 the sentence "All stock
   has been updated by the Sondos team on Trendyol today" appeared on five alerts of three
   different types, including two *profitability* alerts a stock line cannot answer. Diff
   the comment text across the week's batch: five identical comments are one update, not
   five, and the per-AM Updated column will otherwise read as a good week.

   **A task closed with no comment is its own finding.** Dar Sonbol's onboarding card
   closed on 12 Oct after 36 days overdue with nothing written — what completed, what the
   booked call agreed and what carries into v2 are all unrecorded. Closure without a note
   destroys the handover.

   **Flag any task whose status contradicts its comments.** A task marked `running`
   whose only comment says "blocked on client" will land in the wrong column and read as
   progress. Wk 34's Salla-themes task did exactly that. Put these in Update Quality —
   the contradiction is the finding.

   A blocked task must name the person being waited on and the date they were last
   chased. "Pending client" with neither cannot be escalated.

**Scope exclusions — apply everywhere on the page:**

- **Salla revenue for AlFaris Group brands** is outside the AM model. Do not delete the
  Salla row — show the channel at **0** so its absence is explicit rather than looking
  like an oversight. Nokush is the only in-scope brand on Salla.
- **SaaS accounts never appear in the BM WBR** — Lotana Boutique is SaaS. They surface in
  Brand Health automatically, so filter them out by name rather than trusting the list.

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
  The **v2 template is nine phases** — `Phase 0 · Deal Handover` through
  `Phase 8 · Go-Live, Review & Handover` — and first ran on a genuinely new brand
  (Al Safa care) on 13 Oct. Phases carry no individual owner by default; that gap is
  worth stating.
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

- **2026-10-20** — **Put revenue growth next to order growth.** Wk 42 was −32% revenue on
  −7% orders: a basket move (116 → 85 SAR), not a demand move.
- **2026-10-20** — **Check live stock before blaming demand.** Invita's −62% was an Amazon
  stock-out with every SKU at 0 and 450 units inbound, and **no task existed for it**.
  `inventory_live` needs both `brand` and `channel`.
- **2026-10-20** — **A new AM rebases every count.** Nasser added 16 main tasks in one
  week; name who created new cards before reporting list growth, and check for duplicates
  of existing cards (the Sondos POs landed twice).
- **2026-10-20** — **Work migrates to the wrong list** — Tenda's onboarding ran through
  Catalog while Onboarding stayed silent. Report where the work is.
- **2026-10-20** — **A rename in flight breaks week-over-week figures** (Sonbol → Tenda).
  Flag it and ask for the cutover date.
- **2026-10-20** — **An alert closing on a system recovery is not the AM's answer
  landing.** Credit the close, still carry the update as weak.

- **2026-10-13** — **Prior-week sales figures restate downward ~6% over the following
  fortnight.** The `Last wk` column will not match the prior page's `This wk` — compute
  both periods from one `compare_sales_periods` call, then say so on the page.
- **2026-10-13** — **New channels appear without warning** (Namshi, id 14, carrying
  Sonbol's first marketplace revenue). Keep the Total on Amazon · Noon · Trendyol and put
  a new channel in its own row outside it, pending a scope decision.
- **2026-10-13** — **"Resolved in the comment, open on the board" is the commonest AM
  failure mode** — four in one Sunday. Name each; the board is what the WBR counts.
- **2026-10-13** — **Diff comment text across the week's batch.** One sentence pasted onto
  five alerts of three types reads as five updates and is one.
- **2026-10-13** — **A task closed with no comment is its own finding** (Dar Sonbol
  onboarding, 36 days overdue, closed silently).
- **2026-10-13** — **A blank ad card may be a frozen account, not a silent one.** Read the
  comments before calling it neglect, then flag that the freeze is recorded on one card of
  five and carries no review date.
- **2026-10-13** — The v2 onboarding template is **nine phases (0–8)**; Nasser Abuwandah
  `308593216` joined the workspace on Al Safa care.

- **2026-10-06** — **Phase 0's own comments bump `date_updated`.** Discount
  `⏰ WBR Phase 0`, ClickBot `@assignees` and system recovery/escalation notes when
  judging "updated". Wk 40 had 24 tasks with in-window-or-later `date_updated` and zero
  human comments in the window. Bound the comment pull to `date_updated >= window start`.
- **2026-10-06** — **The ad template is three levels deep** since the 21 Sep rebuild:
  `Brand → Ads / Promotions → one card per channel`. 5 brands = **30 channel cards**, all
  unassigned. Stopping at the brand parent undercounts the silence six-fold.
- **2026-10-06** — **Three tests before calling a revenue jump real**: orders moved in
  proportion · the lift is spread across the days · settlements synced. Then say whether
  it fades inside the week. Wk 40's +80% passed all three and still faded 3,117 → 812.
- **2026-10-06** — **Re-test the condition behind every carried escalation.** The Salla
  sync alert had been healthy for weeks and was still on the page as open. Carrying a
  resolved alert is as wrong as missing a real one.
- **2026-10-06** — **Nokush's Salla is in scope and no longer zero.** Own row labelled
  `Salla — Nokush only`, kept outside the marketplace Total for comparability.
- **2026-10-06** — `Brand Health by System` now reads back as **`Brand Health`**, Store
  Enhancement is gone from the space, and new task ids do not start `86ey`. Match on list
  id, never on name or id prefix.
- **2026-10-06** — Phase 0's reminder text was wrong on two counts and was fixed in the
  Routine: it announced a 4:00 PM build when Phase 1 runs 15:30, and it hardcoded "Second
  week in a row" on tasks silent for six. It now counts the streak from the task's own
  comments.

- **2026-08-06** — **Brand Health** splits into `Done | Updated | No Update` with the
  open items grouped *updated / not updated*. **Advertising** is a campaign-level matrix
  (`Active with update | Active no update | Paused`) listing individual levers as
  `Channel lever - Brand`, not counts.
- **2026-08-06** — Onboarding accounts get their own `###` headings.
- **2026-08-06** — **Escalations are the lead's list, not mine.** Wk 31 was cut from 8 to
  2 on the call. Carry forward only what the lead keeps; do not re-add items they removed.
- **2026-08-06** — When the lead says a **system is down**, mark the affected section
  **provisional** and say so at the top of it. Do not report the dip as demand.
- **2026-08-06** — Each list section carries a **per-AM table** —
  `AM | Done | Open | Overdue | Not completed` — with open task names bulleted in the cell.
- **2026-08-06** — **Salla revenue for AlFaris Group is excluded**, shown as an explicit
  **0 row**. Removing it flipped Wk 31 from −35% to **+16%** — not cosmetic, it changes
  the conclusion. **SaaS accounts (Lotana Boutique) never appear.**
- **2026-08-06** — List sections lead with **open vs complete** counts, not "updated".
- **2026-08-06** — **Never write "No update" without opening the task and reading its
  comments.** Partial counts as its own status.
- **2026-08-06** — **The ClickUp API quota is DAILY and account-wide across EVERY
  endpoint — reads, task creation, page updates and page creation all draw on it.**
  Creating a fresh page is not a workaround for a rate-limited update; both fail
  identically. Tested three ways on 6 Aug. It reports as `NaN minutes` on document writes but gives the real
  figure elsewhere: `wait 1302 minutes` (~21.7h). Exhausting it on page revisions locked
  the workspace out of ClickUp entirely, hours before the call the report was for. **Budget the whole session, not the write.** Pull data once and
  cache it in the working notes; never re-pull a list you already have. **Draft the page
  in full and write ONCE** — every revision is a page-sized write against a daily cap.
  If the cap is hit: write the content to a file, hand it to the lead so they can paste
  it themselves, and **stop calling ClickUp** — further attempts only confirm the lock.
  Do not schedule a retry inside the same day; the quota will not have reset.
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
