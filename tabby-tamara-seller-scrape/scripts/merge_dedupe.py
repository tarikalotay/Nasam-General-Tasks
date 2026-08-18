#!/usr/bin/env python3
"""Merge Tabby + Tamara scrapes, dedupe within and across sources."""
import json, re, sys, unicodedata
from urllib.parse import urlparse, parse_qs, unquote

# Hosts that are shorteners/affiliate redirectors — never use for identity
SHORTENERS = {
    "s.noon.com", "ty.gl", "tamara.go.link", "bit.ly", "cutt.ly", "cutt.us",
    "onelink.me", "app.adjust.com", "go.link", "linktr.ee", "taplink.cc",
    "linkin.bio", "beacons.ai", "goo.gl", "tinyurl.com", "shorturl.at",
    "t.co", "s.lazurde.com", "click.linksynergy.com", "smart.link",
}
# Hosts where the store identity lives in the first path segment
PATH_PLATFORMS = {
    "salla.sa", "salla.com", "salla.network", "instagram.com", "wa.me",
    "api.whatsapp.com", "taplink.cc", "linktr.ee", "khamsat.com", "mostaql.com",
}

AR_DIAC = re.compile(r"[ً-ْٰـ]")
NONWORD = re.compile(r"[^0-9a-zء-ي]+")
STOPWORDS = {
    "store", "shop", "stores", "boutique", "online", "official", "sa", "ksa",
    "co", "company", "est", "trading", "متجر", "متاجر", "محل", "مؤسسة", "شركة",
    "معرض", "مركز", "the", "al", "ال",
}

def norm_name(s):
    if not s:
        return ""
    s = unicodedata.normalize("NFKC", str(s)).lower().strip()
    s = AR_DIAC.sub("", s)
    s = s.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ة", "ه").replace("ى", "ي")
    toks = [t for t in NONWORD.split(s) if t and t not in STOPWORDS]
    return "".join(toks)

def clean_url(u):
    if not u:
        return ""
    u = u.strip()
    if not u:
        return ""
    if not re.match(r"^https?://", u, re.I):
        u = "https://" + u
    p = urlparse(u)
    host = (p.netloc or "").lower().split(":")[0]
    if host.startswith("www."):
        host = host[4:]
    if not host or "." not in host:
        return ""
    # strip tracking params
    keep = "&".join(f"{k}={v[0]}" for k, v in parse_qs(p.query).items()
                    if not k.lower().startswith(("utm_", "gclid", "fbclid", "adj_", "mc_")))
    path = p.path.rstrip("/")
    return f"https://{host}{path}" + (f"?{keep}" if keep else "")

def domain_key(u):
    """Identity key for a URL, or '' if it can't identify a store."""
    if not u:
        return ""
    p = urlparse(u if re.match(r"^https?://", u, re.I) else "https://" + u)
    host = (p.netloc or "").lower().split(":")[0]
    if host.startswith("www."):
        host = host[4:]
    if not host or host in SHORTENERS or host.endswith(".go.link") or host.endswith(".onelink.me") or host.endswith(".adj.st"):
        return ""
    if host in PATH_PLATFORMS:
        seg = [s for s in p.path.split("/") if s]
        return f"{host}/{unquote(seg[0]).lower()}" if seg else ""
    return host

def is_arabic(s):
    return bool(s) and bool(re.search(r"[ء-ي]", s))

def load_tabby(path):
    recs = {}
    for line in open(path, encoding="utf-8"):
        r = json.loads(line)
        name = (r.get("name") or "").strip()
        name_ar = (r.get("name_ar") or "").strip()
        name_en = "" if is_arabic(name) else name
        if is_arabic(name) and not name_ar:
            name_ar = name
        url = clean_url(r.get("url") or "")
        cats = sorted({c["t"] for c in (r.get("cats") or []) if c and c.get("t")})
        st = r.get("store_types") or []
        rec = {
            "name_en": name_en, "name_ar": name_ar,
            "website": url,
            "dkey": domain_key(url),
            "cats": set(cats),
            "online": "onlineStore" in st, "instore": "inStore" in st,
            "services": sorted(set(r.get("services") or [])),
            "tabby_link": f"https://tabby.sa/en-SA/shop/stores/{r['slug']}" if r.get("slug") else "",
            "desc": (r.get("desc") or "").strip(),
            "affiliate": bool(r.get("affiliate")),
            "seller_id": r.get("seller_id") or r.get("merchant_id") or r["_id"],
        }
        # dedupe tabby-internal by seller_id first, then by domain, then name
        recs[rec["seller_id"]] = rec
    # collapse same domain/name duplicates within tabby
    merged, by_key = [], {}
    for rec in recs.values():
        key = rec["dkey"] or ("name:" + (norm_name(rec["name_en"]) or norm_name(rec["name_ar"]) or rec["seller_id"]))
        if key in by_key:
            t = by_key[key]
            t["cats"] |= rec["cats"]
            t["online"] |= rec["online"]; t["instore"] |= rec["instore"]
            t["services"] = sorted(set(t["services"]) | set(rec["services"]))
            for f in ("name_en", "name_ar", "website", "tabby_link", "desc"):
                if not t[f] and rec[f]:
                    t[f] = rec[f]
        else:
            by_key[key] = rec
            merged.append(rec)
    return merged

def load_tamara(path):
    by_key = {}
    for line in open(path, encoding="utf-8"):
        r = json.loads(line)
        name = (r.get("name") or "").strip()
        link = clean_url(r.get("link") or "")
        dk = domain_key(link)
        key = dk or ("name:" + norm_name(name))
        if not key or key == "name:":
            continue
        rec = by_key.setdefault(key, {
            "name_en": "", "name_ar": "", "website": "", "raw_link": "",
            "dkey": dk, "cats": set(), "tamara": True,
        })
        rec["cats"].add(r.get("category") or "")
        if r["locale"] == "en_SA":
            if not rec["name_en"] and not is_arabic(name):
                rec["name_en"] = name
            if is_arabic(name) and not rec["name_ar"]:
                rec["name_ar"] = name
        else:
            if is_arabic(name):
                rec["name_ar"] = rec["name_ar"] or name
            elif not rec["name_en"]:
                rec["name_en"] = name
        if not rec["raw_link"] and link:
            rec["raw_link"] = link
        # prefer a real website over shortener
        if dk and not rec["website"]:
            rec["website"] = link
    for rec in by_key.values():
        rec["cats"] = {c for c in rec["cats"] if c}
    return list(by_key.values())

def main():
    tabby = load_tabby("tabby_merchants.jsonl")
    tamara = load_tamara("tamara_stores.jsonl")
    print(f"tabby unique: {len(tabby)}, tamara unique: {len(tamara)}")

    # index tabby by domain key and by normalized names
    by_dkey, by_name = {}, {}
    out = []
    for t in tabby:
        t["sources"] = {"Tabby"}
        t["tamara_cats"] = set()
        out.append(t)
        if t["dkey"]:
            by_dkey.setdefault(t["dkey"], t)
        for n in (norm_name(t["name_en"]), norm_name(t["name_ar"])):
            if n and len(n) >= 4:
                by_name.setdefault(n, t)

    matched = 0
    for m in tamara:
        hit = None
        if m["dkey"] and m["dkey"] in by_dkey:
            hit = by_dkey[m["dkey"]]
        else:
            for n in (norm_name(m["name_en"]), norm_name(m["name_ar"])):
                if n and len(n) >= 4 and n in by_name:
                    hit = by_name[n]
                    break
        if hit:
            matched += 1
            hit["sources"].add("Tamara")
            hit["tamara_cats"] |= m["cats"]
            if not hit["name_ar"] and m["name_ar"]:
                hit["name_ar"] = m["name_ar"]
            if not hit["name_en"] and m["name_en"]:
                hit["name_en"] = m["name_en"]
            if not hit["website"] and (m["website"] or m["raw_link"]):
                hit["website"] = m["website"] or m["raw_link"]
                hit["dkey"] = hit["dkey"] or m["dkey"]
        else:
            m["sources"] = {"Tamara"}
            m["tamara_cats"] = m["cats"]
            m["cats"] = set()
            m.setdefault("website", m.get("raw_link", ""))
            m.setdefault("online", True); m.setdefault("instore", False)
            m.setdefault("services", []); m.setdefault("tabby_link", "")
            m.setdefault("desc", ""); m.setdefault("affiliate", False)
            if not m["website"] and m.get("raw_link"):
                m["website"] = m["raw_link"]
            out.append(m)

    print(f"tamara matched to tabby: {matched}; combined unique: {len(out)}")
    with open("merged.jsonl", "w", encoding="utf-8") as f:
        for r in out:
            r2 = dict(r)
            r2["cats"] = sorted(r["cats"]); r2["tamara_cats"] = sorted(r["tamara_cats"])
            r2["sources"] = sorted(r["sources"])
            r2.pop("raw_link", None); r2.pop("tamara", None)
            f.write(json.dumps(r2, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
