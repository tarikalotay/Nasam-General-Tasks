# Nasam Revenue View — weekly update runbook

Canonical builder for `output/Nasam_Revenue_View.xlsx`. A scheduled routine runs this **every Sunday 10:00 (Riyadh)**.

## Files
- `build.py` — builds the workbook from the sources below. Run: `python3 build.py` (from this directory).
- `rev5.py` — platform GMV snapshot, active brands (mcp_read.revenue). Refresh each run via MCP:
  `SELECT "brandName","channelName", substring("date"::text,1,7) AS ym, SUM("totalRevenue"::numeric), SUM("orderCount") FROM mcp_read.revenue WHERE "date">='2025-11-01' GROUP BY 1,2,3` — replace `REV_ACT`. Also refresh Sonbol's from-integration figure (`add6.SONBOL_FROM_INTEGRATION`, date >= 2026-08-13).
- `old_gmv.py`, `add6.py` — frozen snapshots: churned brands (platform no longer serves deactivated brands) and Two United's constellation (orders view). Do not refresh.
- `fetch_wafeq.py` — pulls all Wafeq invoices/contacts/items/projects to `sources/wafeq_api_snapshot.json`. Needs `ACCOUNTING_API_KEY` in the environment (never committed). Verified working 18 Aug 2026 (160 invoices).
- `sources/` — dated input snapshots: Wafeq invoice export (xlsx), closed-PO export (csv), Salla Partners subscriptions (pdf; data transcribed into `build.py` `SAAS_SUBS`).

## Weekly run (what the routine does)
1. **Wafeq**: run `fetch_wafeq.py` (API). First keyed run: adapt the parser to the API snapshot and reconcile against the last manual export before switching; until then `build.py` reads the xlsx in `sources/`.
2. **Retail**: once the manual PO invoices appear in Wafeq (started 18 Aug — e.g. INV-000192), the to-invoice stream moves to billed automatically via the Wafeq data. New closed POs still come from the PO export until the platform exposes PO values (Q2, with Fahad) — then pull directly from `mcp_read.purchase_orders` and retire the export.
3. **Platform**: refresh `rev5.py` + Sonbol figure via MCP queries above.
4. **Salla subscriptions**: manual Salla Partners export from Tarik; update `SAAS_SUBS` in `build.py` (paid = net ex-VAT after coupon; Salla share 15%).
5. **Build + verify**: `python3 build.py`; re-verify: billed client-month cells vs an independent Wafeq re-parse (must be 0 mismatches), nested rows == client totals, allocation preservation, TOTAL = billed + to-invoice + SaaS net.
6. **Deliver**: send the workbook with a delta summary vs last week (new invoices, POs, subscriptions, totals, Q1–Q4 status). Flag any manual input older than 7 days. Commit and push the refreshed sources + output to `claude/nasam-roadmap-pricing-ob83ez`.

## Reporting rules (fixed decisions)
Window Nov 2025+ (current model) · GMV post-Nasam only (Sonbol from 13 Aug 2026; post-churn months excluded) · SaaS brand-channels 0% commission · SaaS subscriptions net of Salla 15% · Cloud Shelf recharges (3,355.01), Dashcam and the old 35% ledger excluded · retail commission on RECEIVED value, closed POs only · no VAT (exempt, trailing-12m income < 375K).

## Open questions
Q1 retail invoices being raised manually (started 18 Aug) · Q2 PO value columns in platform (Fahad) · Q3 Wafeq API parser switch-over (key verified) · Q4 Salla app trials converting w/c 19 Aug.
