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


INDUSTRY_MAP = [
    ("Fashion & Apparel", {"fashion", "fashion & apparel", "apparel"}),
    ("Beauty & Personal Care", {"beauty & health", "beauty", "health & wellness", "health"}),
    ("Electronics & Tech", {"electronics", "technology & electronics"}),
    ("Home, Furniture & Appliances", {"home & appliances", "home & garden", "home & kitchen"}),
    ("Automotive", {"automotive"}),
    ("Jewellery & Watches", {"jewellery, gold & watches"}),
    ("Kids & Toys", {"kids & toys"}),
    ("Grocery & Supermarket", {"supermarket", "grocery & food"}),
    ("Sports & Fitness", {"fitness & outdoor", "fitness & outdoors"}),
    ("Flowers & Gifts", {"flowers & gifts"}),
    ("Pets", {"pets"}),
    ("Arts & Crafts", {"arts & crafts"}),
    ("Collectibles & Hobbies", {"anime & collectibles"}),
    ("General Retail", {"retail & consumer goods", "others"}),
    ("Healthcare Services (Clinics)", {"clinics"}),
    ("Beauty Services (Salons & Spas)", {"salons & spas"}),
    ("Education & Training", {"training & courses", "educational services", "education"}),
    ("Travel & Tourism", {"travel", "hospitality & travel"}),
    ("Food Service & Restaurants", {"restaurants", "meal plans", "food & beverage"}),
    ("Insurance & Finance", {"insurance"}),
    ("Entertainment & Leisure", {"entertainment", "entertainment & leisure"}),
    ("Professional Services", {"personal & professional services"}),
    ("Marketplace", {"marketplace"}),
]

def industry_of(cats):
    low = {c.lower() for c in cats}
    for label, keys in INDUSTRY_MAP:
        if low & keys:
            return label
    return "Unclassified"

def potential(row):
    """0-100 lead-potential score; components documented in the Summary sheet."""
    s = 0
    if row["Website Status"] == "ok":
        s += 30
    elif row["Website"]:
        s += 10
    if row["Emails"]:
        s += 25
    if row["Phone Numbers"] or row["WhatsApp"]:
        s += 10
    if row["Instagram"] or row["Twitter/X"] or row["TikTok"] or row["Snapchat"]:
        s += 10
    if row["On Tabby"] and row["On Tamara"]:
        s += 10
    if "physical" in row["Online Presence"]:
        s += 5
    if "Online" in row["Online Presence"]:
        s += 10
    return s

def tier(score):
    return "High" if score >= 65 else ("Medium" if score >= 40 else "Low")

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
    FIELDS = ("emails", "phones", "whatsapp", "instagram", "twitter",
              "tiktok", "snapchat", "linkedin")
    contacts = {}
    try:
        for line in open(CONTACTS, encoding="utf-8"):
            c = json.loads(line)
            prev = contacts.get(c["dkey"])
            if prev is None:
                contacts[c["dkey"]] = c
                continue
            # union contact data across attempts; keep the successful status
            for f in FIELDS:
                merged = sorted(set(prev.get(f) or []) | set(c.get(f) or []))
                prev[f] = merged[:6]
            if prev.get("status") != "ok" and c.get("status") == "ok":
                prev["status"] = "ok"
                prev["final_url"] = c.get("final_url") or prev.get("final_url", "")
    except FileNotFoundError:
        pass

    rows_ok, rows_no = [], []
    for line in open(MERGED, encoding="utf-8"):
        r = json.loads(line)
        ok, reason = classify(r)
        c = dict(contacts.get(r.get("dkey") or "", {}))
        # If the "website" itself is a social/WhatsApp link, derive the handle directly
        dk = r.get("dkey") or ""
        host, _, seg = dk.partition("/")
        if seg:
            if host == "instagram.com":
                c["instagram"] = sorted(set(c.get("instagram") or []) | {seg})
            elif host in ("wa.me", "api.whatsapp.com") and re.fullmatch(r"\+?\d{9,15}", seg):
                c["whatsapp"] = sorted(set(c.get("whatsapp") or []) | {"+" + seg.lstrip("+")})
        ig = c.get("instagram") or []
        cats = sorted(set(r["cats"]) | set(r["tamara_cats"]))
        row = {
            "Store Name (EN)": r["name_en"],
            "Store Name (AR)": r["name_ar"],
            "Industry": industry_of(cats),
            "Potential": "",
            "Potential Score": 0,
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
        row["Potential Score"] = potential(row)
        row["Potential"] = tier(row["Potential Score"])
        if ok:
            rows_ok.append(row)
        else:
            row2 = {"Store Name (EN)": row["Store Name (EN)"],
                    "Store Name (AR)": row["Store Name (AR)"],
                    "Reason Not Eligible": reason}
            row2.update({k: v for k, v in row.items() if k not in row2})
            rows_no.append(row2)

    def sort_key(row):
        return (-row["Potential Score"], (row["Store Name (EN)"] or row["Store Name (AR)"]).lower())
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
