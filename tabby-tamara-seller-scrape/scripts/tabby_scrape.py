#!/usr/bin/env python3
"""Scrape all KSA merchants from Tabby's public Sanity CMS dataset."""
import json, sys, time, urllib.parse, urllib.request

BASE = "https://cbjxg0yl.apicdn.sanity.io/v2023-08-01/data/query/production_v2?query="
OUT = sys.argv[1] if len(sys.argv) > 1 else "tabby_merchants.jsonl"
PAGE = 1000

def q(groq, retries=5):
    url = BASE + urllib.parse.quote(groq)
    for i in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=90) as r:
                return json.load(r)["result"]
        except Exception as e:
            if i == retries - 1:
                raise
            time.sleep(2 ** i)

def fetch_lang(lang):
    rows, last_id = [], ""
    proj = ("{_id,'name':content.main.merchant_display_name,"
            "'merchant_id':content.main.merchant_id,'seller_id':content.main.seller_id,"
            "'url':content.main.merchant_url,'slug':content.main.slug.current,"
            "'affiliate':content.main.isAffiliate,'services':content.main.service_type,"
            "'store_types':content.bnpl.store_types,"
            "'cats':content.main.category[]->{'t':coalesce(countryDependentNames.ksa,title,name)},"
            "'desc':content.main.store_short_description}")
    while True:
        groq = (f"*[_type=='merchant' && content.main.country=='ksa' && __i18n_lang=='{lang}'"
                f" && _id>'{last_id}']|order(_id asc)[0..{PAGE-1}]{proj}")
        batch = q(groq)
        if not batch:
            break
        rows.extend(batch)
        last_id = batch[-1]["_id"]
        print(f"  {lang}: {len(rows)} fetched", flush=True)
        if len(batch) < PAGE:
            break
    return rows

def main():
    en = fetch_lang("en")
    ar = fetch_lang("ar")
    # Arabic docs share the base _id with an __i18n_ar suffix; also key by seller_id
    ar_by_base = {}
    for r in ar:
        base = r["_id"].replace("__i18n_ar", "")
        ar_by_base[base] = r
    merged, seen_ar = [], set()
    for r in en:
        a = ar_by_base.get(r["_id"])
        if a:
            r["name_ar"] = a.get("name")
            if not r.get("url") and a.get("url"):
                r["url"] = a.get("url")
            seen_ar.add(a["_id"])
        merged.append(r)
    # Arabic-only merchants with no English counterpart
    for r in ar:
        if r["_id"] not in seen_ar:
            r["name_ar"] = r.get("name")
            merged.append(r)
    with open(OUT, "w", encoding="utf-8") as f:
        for r in merged:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"total en={len(en)} ar={len(ar)} merged={len(merged)} -> {OUT}")

if __name__ == "__main__":
    main()
