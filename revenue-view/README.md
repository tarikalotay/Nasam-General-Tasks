# Nasam Revenue View — weekly update runbook

Canonical builder for `output/Nasam_Revenue_View.xlsx`. A scheduled routine runs this **every Sunday 10:00 (Riyadh)**.

## Files
- `build.py` — builds the workbook from the sources below. Run: `python3 build.py` (from this directory).
- `rev5.py` — platform GMV snapshot, active brands (mcp_read.revenue). Refresh each run via MCP:
  `SELECT "brandName","channelName", substring("date"::text,1,7) AS ym, SUM("totalRevenue"::numeric), SUM("orderCount") FROM mcp_read.revenue WHERE "date">='2025-11-01' GROUP BY 1,2,3` — replace `REV_ACT`. Also refresh Sonbol's from-integration figure (`add6.SONBOL_FROM_INTEGRATION`, date >= 2026-08-13).
- `old_gmv.py`, `add6.py` — frozen snapshots: churned brands (platform no longer serves deactivated brands) and Two United's constellation (orders view). Do not refresh.
- `fetch_wafeq.py` — pulls all Wafeq invoices/contacts/items/projects to `sources/wafeq_api_snapshot.json`. Needs `ACCOUNTING_API_KEY` in the environment (never committed). Verified working 18 Aug 2026 (160 invoices).
- `chart_invoices_by_stream.py` — renders `output/nasam_invoices_by_stream.png`: invoiced revenue by month, stacked by AM fees / commission / setup, discounts below the baseline. Figures come from the by-stream aggregation of every issued invoice.
- `mapping.py` — the platform's own commercial mapping per organization: the per-channel commission toggle (العمولة سارية / بلا عمولة) and the monthly fee (الرسوم الشهرية), as set in تعديل المنظمة. This is now the authority on whether a channel is invoiced; the rate card is the fallback for organizations not yet read. `validate()` holds the mapping against the billing and returns the findings shown as PLATFORM MAPPING CHECK on sheet 1. Only organizations actually read off the platform go in `ORGS` — nothing is inferred, and everything else is reported as unconfirmed.
- `accounting.py` — the expense side: parses the monthly Wafeq bills and journal exports plus the customer-balances statement into the monthly series behind sheet 4 (`Cost & Break-even`). Classifies bill accounts as Nasam's own cost or spent on a client's behalf (`CLIENT_SIDE`).
- `sources/` — dated input snapshots: Wafeq invoice export (xlsx), closed-PO export (csv), Salla Partners subscriptions (pdf; data transcribed into `build.py` `SAAS_SUBS`), and the monthly accounting drop (bills, journal, AR statement).

## Weekly run (what the routine does)
1. **Wafeq**: run `fetch_wafeq.py` (API). First keyed run: adapt the parser to the API snapshot and reconcile against the last manual export before switching; until then `build.py` reads the xlsx in `sources/`.
2. **Retail**: once the manual PO invoices appear in Wafeq (started 18 Aug — e.g. INV-000192), the to-invoice stream moves to billed automatically via the Wafeq data. New closed POs still come from the PO export until the platform exposes PO values (Q2, with Fahad) — then pull directly from `mcp_read.purchase_orders` and retire the export.
3. **Platform**: refresh `rev5.py` + Sonbol figure via MCP queries above.
4. **Platform mapping**: refresh `mapping.py` — for each organization, the per-channel commission flag and the monthly fee — then move `AS_OF`. Nasam fixed this mapping in the platform in Sep 2026, so a channel is commissioned only if the platform says it is. A channel set to بلا عمولة still syncs its orders and still counts in sales; only its commission leaves the invoice — never drop its GMV. Read the mapping every run: it is a switch Nasam flips, and flipping it changes what should be invoiced next month. The check then reports, per brand-channel: commission active with sales but nothing billed, commission off yet billed anyway, a platform flag that contradicts the rate card, and a platform monthly fee that is not being billed.
5. **Salla subscriptions**: manual Salla Partners export from Tarik; update `SAAS_SUBS` in `build.py` (paid = net ex-VAT after coupon; Salla share 15%).
6. **Build + verify**: `python3 build.py`; re-verify: billed client-month cells vs an independent Wafeq re-parse (must be 0 mismatches), nested rows == client totals, allocation preservation, TOTAL = billed + to-invoice + SaaS net. Read the mapping check and carry anything marked "Decide" into the delivery note.
7. **Deliver**: send the workbook with a delta summary vs last week (new invoices, POs, subscriptions, totals, Q1–Q4 status). Flag any manual input older than 7 days. Commit and push the refreshed sources + output to `claude/nasam-roadmap-pricing-ob83ez`.

## Monthly close (first week of each month, after the invoices are released)

Tarik releases the monthly invoices at the start of the month and then shares four Wafeq exports (data to the previous day). The first run after that drop is the monthly close — do these on top of the weekly steps:

1. **Drop the exports into `sources/`** with the export date in the name, and update the AR statement JSON from the PDF:
   `wafeq_invoices_<date>.xlsx` · `wafeq_bills_<date>.xlsx` · `wafeq_journal_<date>.xlsx` · `wafeq_ar_statement_<date>.pdf` + `ar_statement_<date>.json` (rows transcribed: contact, client, debit, credit, closing; check the rows tie to debit less credit before trusting the footer).
2. **Released invoices**: re-run `fetch_wafeq.py`. Invoices that were DRAFT last week should now be SENT — they leave the "drafted, not yet issued" memo row and enter billed. Report the amount that moved, and any invoice whose amount changed on release (a dropped fee or a discount).
3. **Cost and funding** (`accounting.py`, sheet 4): salaries from journal accounts 5201/5231, own cost from the bills, client-side spend kept separate (ads, prep, shipping, marketplace fees) until each line is confirmed as rebilled or absorbed, partner contributions from 3231-3234, Monshaat from 421, Salla payouts from 418. New expense accounts appear automatically; check any that should be reclassified as client-side in `accounting.CLIENT_SIDE`.
4. **Receivables**: reconcile Wafeq live balances against the accountant's statement per client. Differences are receipts or credits booked in the ledger but not applied to the invoices in Wafeq — list them; they are collections work, not data errors.
5. **Report the close**: revenue against operating cost for the closed month, cost covered by revenue, the funding drawn, and the receivables gap.

Weekly runs in between do not refresh the cost sheet. It keeps the drop it was built from, and the ReadMe sheet names that date.

## Reporting rules (fixed decisions)
Window Nov 2025+ (current model) · GMV post-Nasam only (Sonbol from 13 Aug 2026; post-churn months excluded) · a channel carries commission only if the platform mapping says so — بلا عمولة means 0% commission while the orders keep syncing and keep counting in sales; organizations not yet read off the platform fall back to the rate card, where SaaS brand-channels are 0% · SaaS subscriptions net of Salla 15% · pass-throughs excluded — Cloud Shelf recharges (3,355.01 in window) and marketing rebilled to a client at cost (INV-000137, 16,534.40, Oct 2025); only a management fee charged on such work is revenue, and that invoice carried none — Dashcam and the old 35% ledger excluded · retail commission on RECEIVED value, closed POs only · no VAT (exempt, trailing-12m income < 375K).

## Open questions
Q1 retail invoices being raised manually (started 18 Aug) · Q2 PO value columns in platform (Fahad) · Q3 Wafeq API parser switch-over (key verified, now the source) · Q4 Salla app trials converting w/c 19 Aug · Q5 which client-side spend is rebilled and which is absorbed (sheet 4) · Q6 the accountant's statement footer does not tie to its own rows (4,217.68) · Q7 receipts booked in the ledger but not applied to invoices in Wafeq (17,545.95 as of 8 Sep) · Q8 Sonbol's platform monthly fee is 8,000 but the rate card says 5,000 with 50% at the first live managed channel, and nothing has been billed — which figure applies, and from when · Q9 the platform read layer needs re-authorising before the remaining 20 brands can be read off the platform instead of the rate card.
