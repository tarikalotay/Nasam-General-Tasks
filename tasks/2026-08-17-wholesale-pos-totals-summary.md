# Wholesale › Purchase Orders — totals summary strip

**Date:** 2026-08-17
**Requested by:** Tarik (screenshot of live Purchase Orders page: "lets add total… make sure to do UX touch")

## Agreed spec

A summary strip between the filter bar and the PO table, aggregating the **entire filtered set** (all pages, not just the visible page):

| Stat | Definition |
| --- | --- |
| Total Units | Sum of requested units across filtered POs |
| Total Requested | Sum of requested value (SAR), table's money formatting |
| Fill Rate | Received units ÷ requested units (weighted aggregate, not an average of per-PO Fulfill %) |
| Acceptance Rate | Confirmed/accepted units ÷ requested units ("conform rate"), weighted aggregate |

Requirements: recompute on **every** filter change (search, vendor multi-select, FC, status, brand/channel selectors, date-range chips); skeleton loading states; "—" instead of divide-by-zero on empty sets; 2×2 wrap on narrow screens; RTL/Arabic labels per app i18n; reuse existing stat/KPI design-system components.

## Where the implementation lives

This repo only tracks the task — the code changes are on branch `claude/wholesale-pos-totals-ux` in:

- **Frontend:** `Nasam-co/nasam-frontend-v2` — summary strip on the Purchase Orders page
- **Backend:** `Nasam-co/nasam` — totals computed server-side with the same filters (PO list is server-paginated)

Implemented in Claude session "Wholesale POs — totals summary strip" (`session_01SPdoHaobzHniAzqaN99d9X`); its final status: totals summary bar shipped on both backend & frontend, tests pass. No PRs opened (not requested).
