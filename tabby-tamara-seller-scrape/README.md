# Tabby & Tamara (KSA) — Seller Directory Scrape for Nasam

Lead list of every merchant listed in the Saudi Arabia directories of **Tabby**
(https://tabby.sa/en-SA/shop) and **Tamara** (https://tamara.co/ar-sa/stores),
deduplicated across both platforms, enriched with contact info scraped from each
seller's own website, and classified for Nasam eligibility.

Scrape date: **2026-08-18**.

## Deliverables

| File | What it is |
|---|---|
| `Tabby_Tamara_KSA_Sellers_for_Nasam.xlsx` | Final workbook: `Summary`, `Eligible for Nasam`, and `Not Eligible` sheets |
| `data/eligible.csv` | Same rows as the "Eligible for Nasam" sheet (UTF-8 with BOM, Excel-safe) |
| `data/not_eligible.csv` | Same rows as the "Not Eligible" sheet, with a per-row reason |

## Columns

Store Name (EN/AR), Website, Emails, Phone Numbers, WhatsApp, Instagram, Twitter/X,
TikTok, Snapchat, Categories, Online Presence, On Tabby, On Tamara,
Tabby Directory Link, BNPL Services, Website Status, Description — plus
**Reason Not Eligible** on the not-eligible sheet.

## Method

1. **Tabby** (`scripts/tabby_scrape.py`) — Tabby's shop directory is served from a public
   Sanity CMS dataset. All `merchant` documents with `country == 'ksa'` are pulled in both
   English and Arabic (23,391 unique merchants), including name, URL, slug, categories,
   store types (online / in-store) and BNPL services.
2. **Tamara** (`scripts/tamara_scrape.py`) — Tamara's stores page calls a public API
   (`api.tamara.co/v2/stores/categories`). All categories are paged through for
   `country=sa` in both `en_SA` and `ar_SA` locales (3,842 unique stores).
3. **Merge & dedupe** (`scripts/merge_dedupe.py`) — URLs are normalized (tracking params
   stripped, shortener/affiliate hosts ignored for identity, path-based platforms like
   `salla.sa/<store>` keyed by path). Merchants are deduplicated within each source and
   matched across sources by domain, then by normalized EN/AR name. Result: **25,207 unique
   sellers** (931 listed on both platforms).
4. **Contact enrichment** (`scripts/crawl_contacts.py`) — each unique seller website
   (17,688 domains) is fetched (homepage, plus contact page when the homepage has no email)
   and public emails, Saudi phone numbers, WhatsApp numbers and social handles are extracted.
5. **Eligibility & export** (`scripts/classify_export.py`, `scripts/build_workbook.py`).

## Eligibility criteria used

**Eligible** — product retail businesses Nasam can onboard and manage across Saudi
e-commerce marketplaces: physical consumer products (fashion, beauty, electronics, home,
automotive, toys, grocery, jewellery, pets, …), independent brand/retailer. In-store-only
product retailers are kept and flagged — they are prime "help them go online" prospects.

**Not eligible** (separate sheet, reason per row):
- Marketplace platforms / global giants (Amazon, Noon, Trendyol, AliExpress, Temu, SHEIN,
  IKEA, Carrefour, airlines / OTAs …) — not individual sellers Nasam would onboard.
- Pure service businesses: clinics, salons & spas, education/training, travel & tourism,
  restaurants / meal plans, insurance / financial services, entertainment & leisure,
  personal & professional services.
- Sellers with both product and service categories stay in the Eligible sheet.

## Reproducing

```bash
cd scripts
python3 tabby_scrape.py tabby_merchants.jsonl
python3 tamara_scrape.py tamara_stores.jsonl
python3 merge_dedupe.py            # -> merged.jsonl
python3 crawl_contacts.py 80       # -> contacts.jsonl (long-running)
python3 classify_export.py         # -> eligible.csv, not_eligible.csv
python3 build_workbook.py          # -> Tabby_Tamara_KSA_Sellers_for_Nasam.xlsx
```
