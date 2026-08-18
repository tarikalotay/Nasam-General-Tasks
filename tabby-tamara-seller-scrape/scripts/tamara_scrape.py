#!/usr/bin/env python3
"""Scrape all SA stores from Tamara's public stores API."""
import json, sys, time, urllib.parse, urllib.request

API = "https://api.tamara.co"
TOKEN = "KtOkSRPTx8byHw0h21ikSTG3ca0a00Yxe3Fy"
OUT = sys.argv[1] if len(sys.argv) > 1 else "tamara_stores.jsonl"

def get(path, locale, retries=5):
    req = urllib.request.Request(API + path, headers={
        "Content-type": "application/json",
        "X-Locale": locale,
        "X-Tamara-Token": TOKEN,
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)",
    })
    for i in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            if i == retries - 1:
                raise
            time.sleep(2 ** i)

def fetch_locale(locale):
    cats = get("/v2/stores/categories?country=sa&limit=100&page=1", locale)
    out = []
    for c in cats["data"]:
        cid, cname = c["category_id"], c["category_name"]
        page, per, got = 1, 100, 0
        while True:
            d = get(f"/v2/stores/categories/{cid}?country=sa&limit={per}&page={page}", locale)
            stores = d.get("data") or []
            total = d.get("total", 0)
            for s in stores:
                out.append({"category_id": cid, "category": cname,
                            "name": s.get("name"), "link": s.get("link"),
                            "tag": s.get("tag_label"), "locale": locale})
            got += len(stores)
            print(f"  [{locale}] {cname}: page {page}, +{len(stores)} ({got}/{total})", flush=True)
            if not stores or got >= total or page > 200:
                break
            page += 1
    return out

def main():
    rows = fetch_locale("en_SA") + fetch_locale("ar_SA")
    with open(OUT, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"total rows={len(rows)} -> {OUT}")

if __name__ == "__main__":
    main()
