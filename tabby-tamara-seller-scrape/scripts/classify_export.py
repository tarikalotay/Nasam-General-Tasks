#!/usr/bin/env python3
"""Classify merchants for Nasam eligibility, merge crawled contacts, export CSVs + XLSX."""
import csv, json, re, unicodedata

MERGED, CONTACTS = "merged.jsonl", "contacts.jsonl"

SERVICE_CATS = {
    "clinics": "Healthcare / clinic services",
    "salons & spas": "Salon & spa services",
    "training & courses": "Education / training services",
    "educational services": "Education / training services",
    "education": "Education / training services",
    "travel": "Travel & tourism services",
    "hospitality & travel": "Travel & tourism services",
    "restaurants": "Restaurant / food service",
    "meal plans": "Meal-plan / food subscription service",
    "food & beverage": "Food & beverage service",
    "insurance": "Insurance / financial services",
    "entertainment": "Entertainment / leisure services",
    "entertainment & leisure": "Entertainment / leisure services",
    "personal & professional services": "Personal / professional services",
    "marketplace": "Marketplace platform (aggregator, not an individual seller)",
}
PRODUCT_CATS = {
    "fashion", "beauty & health", "home & appliances", "electronics", "automotive",
    "supermarket", "fitness & outdoor", "fitness & outdoors", "flowers & gifts",
    "kids & toys", "pets", "arts & crafts", "anime & collectibles",
    "fashion & apparel", "retail & consumer goods", "health & wellness",
    "technology & electronics", "home & garden", "jewellery, gold & watches",
    "home & kitchen", "beauty", "grocery & food", "apparel", "health", "others",
}
# Global marketplaces / platform giants — not individual sellers Nasam would onboard
PLATFORMS = {
    "amazon", "noon", "trendyol", "aliexpress", "temu", "banggood", "shein",
    "ebay", "fordeal", "alibaba", "dhgate", "wish", "walmart", "etsy", "namshi",
    "carrefour", "ikea", "flynas", "flyadeal", "saudia", "almosafer", "wego",
    "booking", "agoda", "airbnb", "aljazeeraairways", "rehlat",
}
PLATFORM_DOMAINS = {
    "amazon.sa", "amazon.com", "noon.com", "trendyol.com", "aliexpress.com",
    "temu.com", "banggood.com", "shein.com", "ebay.com", "fordeal.com",
    "alibaba.com", "dhgate.com", "walmart.com", "etsy.com", "namshi.com",
    "carrefourksa.com", "ikea.com.sa", "flynas.com", "flyadeal.com",
    "saudia.com", "almosafer.com", "wego.com", "sa.wego.com", "booking.com",
}

def nrm(s):
    s = unicodedata.normalize("NFKC", (s or "")).lower()
    return re.sub(r"[^0-9a-zء-ي]+", "", s)

def classify(r):
    name_n = nrm(r["name_en"]) or nrm(r["name_ar"])
    dom = (r.get("dkey") or "").split("/")[0]
    if dom in PLATFORM_DOMAINS or name_n in PLATFORMS:
        return False, "Marketplace / global platform — not an individual seller Nasam would onboard"
    cats = {c.lower() for c in (r["cats"] + r["tamara_cats"])}
    svc = {SERVICE_CATS[c] for c in cats if c in SERVICE_CATS}
    prod = {c for c in cats if c in PRODUCT_CATS}
    if svc and not prod:
        return False, "; ".join(sorted(svc))
    return True, ""

def presence(r):
    if r.get("online") or r.get("website"):
        return "Online store" + (" + physical store" if r.get("instore") else "")
    if r.get("instore"):
        return "In-store only (no online store yet)"
    return "Unknown"

def main():
    contacts = {}
    try:
        for line in open(CONTACTS, encoding="utf-8"):
            c = json.loads(line)
            contacts[c["dkey"]] = c
    except FileNotFoundError:
        pass

    rows_ok, rows_no = [], []
    for line in open(MERGED, encoding="utf-8"):
        r = json.loads(line)
        ok, reason = classify(r)
        c = contacts.get(r.get("dkey") or "", {})
        ig = c.get("instagram") or []
        cats = sorted(set(r["cats"]) | set(r["tamara_cats"]))
        row = {
            "Store Name (EN)": r["name_en"],
            "Store Name (AR)": r["name_ar"],
            "Website": r.get("website", ""),
            "Emails": ", ".join(c.get("emails") or []),
            "Phone Numbers": ", ".join(c.get("phones") or []),
            "WhatsApp": ", ".join(c.get("whatsapp") or []),
            "Instagram": ", ".join("https://instagram.com/" + h for h in ig[:2]),
            "Twitter/X": ", ".join((c.get("twitter") or [])[:2]),
            "TikTok": ", ".join((c.get("tiktok") or [])[:2]),
            "Snapchat": ", ".join((c.get("snapchat") or [])[:2]),
            "Categories": ", ".join(cats),
            "Online Presence": presence(r),
            "On Tabby": "Yes" if "Tabby" in r["sources"] else "",
            "On Tamara": "Yes" if "Tamara" in r["sources"] else "",
            "Tabby Directory Link": r.get("tabby_link", ""),
            "BNPL Services": ", ".join(r.get("services") or []),
            "Website Status": c.get("status", "not crawled") if r.get("website") else "no website",
            "Description": (r.get("desc") or "")[:200],
        }
        if ok:
            rows_ok.append(row)
        else:
            row2 = {"Store Name (EN)": row["Store Name (EN)"],
                    "Store Name (AR)": row["Store Name (AR)"],
                    "Reason Not Eligible": reason}
            row2.update({k: v for k, v in row.items() if k not in row2})
            rows_no.append(row2)

    def sort_key(row):
        has_email = 0 if row["Emails"] else 1
        has_site = 0 if row["Website"] else 1
        return (has_email, has_site, (row["Store Name (EN)"] or row["Store Name (AR)"]).lower())
    rows_ok.sort(key=sort_key)
    rows_no.sort(key=sort_key)

    for path, rows in (("eligible.csv", rows_ok), ("not_eligible.csv", rows_no)):
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
    print(f"eligible: {len(rows_ok)}, not eligible: {len(rows_no)}")
    with_email = sum(1 for r in rows_ok if r["Emails"])
    with_phone = sum(1 for r in rows_ok if r["Phone Numbers"] or r["WhatsApp"])
    print(f"eligible with email: {with_email}, with phone/whatsapp: {with_phone}")

if __name__ == "__main__":
    main()
