# Nasam-General-Tasks

## PO commission invoicing (Jul 19 – Aug 6, 2026)

Closed purchase orders for Marah, SONDOS, and Wadi Halfa, sorted by brand, with
per-PO commission invoices for the clients that have a commission rate on file.

### Files

- `pos_sorted_by_brand.csv` — all 23 closed PO rows sorted by brand (Marah,
  SONDOS, Wadi Halfa), then by PO date. Includes units, requested/received SAR,
  accept/fulfill %, outcome, and the computed commission per PO.
- `invoices/wadi_halfa/` — 9 invoices (one per PO) at **4%** commission.
- `invoices/sondos/` — 6 invoices (one per PO) at **6%** commission.
- `invoices/invoices_summary.csv` — one row per invoice with per-client totals:
  **Wadi Halfa SAR 279.97**, **SONDOS SAR 50.04**.
- `generate_invoices.py` — regenerates every file above (`python3 generate_invoices.py`).

### Assumptions

- Commission is charged on the **received (fulfilled) value** of each PO, not
  the requested value; amounts are SAR, exclusive of VAT.
- Rejected POs (`5EOBBQRQ`, `8ZI1SK8E`) received 0 units, so their invoices are
  issued at SAR 0.00 for the record.
- **Marah has no commission rate on file**, so no Marah invoices were
  generated. Its POs are still listed in `pos_sorted_by_brand.csv`; add its
  rate to `COMMISSION_RATES` in `generate_invoices.py` and rerun to produce them.
- PO headers (numbers, brands, channels, dates, fulfillment centers) were
  verified against the Nasam `purchase_orders` data; requested/received amounts
  come from the Nasam PO screen.
