#!/usr/bin/env python3
"""Crawl merchant websites for public contact info (emails, phones, socials)."""
import json, re, ssl, sys, threading, queue, gzip, io, zlib
import urllib.request, urllib.error
from urllib.parse import urljoin, urlparse

IN, OUT = "merged.jsonl", "contacts.jsonl"
WORKERS = int(sys.argv[1]) if len(sys.argv) > 1 else 80
TIMEOUT = 12
MAX_BYTES = 700_000

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
BAD_EMAIL = re.compile(
    r"(\.png|\.jpe?g|\.gif|\.webp|\.svg|\.css|\.js)$|"
    r"@(example|sentry|wixpress|sentry-next|placeholder|email|domain|yourdomain|test|2x|3x)\.|"
    r"^(noreply|no-reply|donotreply)@|@[0-9.]+$", re.I)
PHONE_RE = re.compile(r"(?:\+?966|00966|0)\s?5\d{2}[\s-]?\d{3}[\s-]?\d{3,4}|(?:\+?966)?\s?9200\d{5}|8001\d{6}|\+?966\s?1\d{8}")
TEL_RE = re.compile(r'href=["\']tel:([^"\']+)', re.I)
MAILTO_RE = re.compile(r'href=["\']mailto:([^"\'?]+)', re.I)
WA_RE = re.compile(r'(?:wa\.me|api\.whatsapp\.com/send[^"\']*phone=)[/=]?(\+?\d{9,15})', re.I)
SOCIAL_RES = {
    "instagram": re.compile(r'instagram\.com/([A-Za-z0-9_.]{2,30})', re.I),
    "twitter": re.compile(r'(?:twitter|x)\.com/([A-Za-z0-9_]{2,15})', re.I),
    "tiktok": re.compile(r'tiktok\.com/@([A-Za-z0-9_.]{2,24})', re.I),
    "snapchat": re.compile(r'snapchat\.com/add/([A-Za-z0-9_.-]{2,30})', re.I),
    "linkedin": re.compile(r'linkedin\.com/(?:company|in)/([A-Za-z0-9_-]{2,60})', re.I),
}
SOCIAL_JUNK = {"p", "reel", "reels", "explore", "share", "accounts", "intent", "home",
               "hashtag", "sharer", "login", "search", "wix", "instagram", "twitter",
               "x", "tiktok", "snapchat", "share.php", "widgets"}
CONTACT_HINT = re.compile(r'href=["\']([^"\']*(?:contact|contactus|contact-us|reach-us|support|help-center|تواصل|اتصل|الاتصال|about-us|aboutus)[^"\']*)["\']', re.I)

ctx = ssl.create_default_context()
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
        "Accept-Language": "en,ar;q=0.8", "Accept-Encoding": "gzip, deflate"})
    with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as r:
        raw = r.read(MAX_BYTES)
        enc = (r.headers.get("Content-Encoding") or "").lower()
        if "gzip" in enc:
            try: raw = gzip.GzipFile(fileobj=io.BytesIO(raw)).read(MAX_BYTES)
            except Exception: pass
        elif "deflate" in enc:
            try: raw = zlib.decompress(raw)
            except Exception:
                try: raw = zlib.decompress(raw, -zlib.MAX_WBITS)
                except Exception: pass
        return r.geturl(), raw.decode("utf-8", "ignore")

def extract(html, acc):
    for m in MAILTO_RE.findall(html):
        e = m.strip().lower()
        if e and not BAD_EMAIL.search(e): acc["emails"].add(e)
    for m in EMAIL_RE.findall(html):
        e = m.strip(".").lower()
        if not BAD_EMAIL.search(e) and len(e) < 60: acc["emails"].add(e)
    for m in TEL_RE.findall(html):
        p = re.sub(r"[^\d+]", "", m)
        if 9 <= len(p.lstrip("+")) <= 14: acc["phones"].add(p)
    for m in PHONE_RE.findall(html):
        p = re.sub(r"[^\d+]", "", m)
        if 9 <= len(p.lstrip("+")) <= 14: acc["phones"].add(p)
    for m in WA_RE.findall(html):
        acc["whatsapp"].add(m if m.startswith("+") else "+" + m.lstrip("0"))
    for key, rx in SOCIAL_RES.items():
        for m in rx.findall(html):
            h = m.lower().strip(".")
            if h not in SOCIAL_JUNK and not h.startswith("share"):
                acc[key].add(h)

def process(rec):
    url = rec["website"]
    acc = {k: set() for k in ("emails", "phones", "whatsapp", *SOCIAL_RES)}
    status, final = "error", ""
    try:
        final, html = fetch(url)
        status = "ok"
        extract(html, acc)
        if not acc["emails"]:
            hints = CONTACT_HINT.findall(html)[:2]
            for h in hints:
                try:
                    _, h2 = fetch(urljoin(final, h))
                    extract(h2, acc)
                    if acc["emails"]: break
                except Exception: pass
    except urllib.error.HTTPError as e:
        status = f"http_{e.code}"
    except Exception as e:
        status = type(e).__name__
    return {"dkey": rec["dkey"], "website": url, "status": status, "final_url": final,
            **{k: sorted(v)[:6] for k, v in acc.items()}}

def main():
    seen, jobs = set(), []
    for line in open(IN, encoding="utf-8"):
        r = json.loads(line)
        if r.get("website") and r.get("dkey") and r["dkey"] not in seen:
            seen.add(r["dkey"]); jobs.append({"dkey": r["dkey"], "website": r["website"]})
    done = set()
    try:
        for line in open(OUT, encoding="utf-8"):
            try: done.add(json.loads(line)["dkey"])
            except Exception: pass
    except FileNotFoundError: pass
    jobs = [j for j in jobs if j["dkey"] not in done]
    print(f"domains to crawl: {len(jobs)} (already done: {len(done)})", flush=True)
    qq = queue.Queue()
    for j in jobs: qq.put(j)
    lock = threading.Lock()
    out = open(OUT, "a", encoding="utf-8")
    count = [len(done)]
    def worker():
        while True:
            try: j = qq.get_nowait()
            except queue.Empty: return
            res = process(j)
            with lock:
                out.write(json.dumps(res, ensure_ascii=False) + "\n")
                count[0] += 1
                if count[0] % 250 == 0:
                    out.flush(); print(f"progress: {count[0]}", flush=True)
    threads = [threading.Thread(target=worker, daemon=True) for _ in range(WORKERS)]
    for t in threads: t.start()
    for t in threads: t.join()
    out.close()
    print("crawl complete", flush=True)

if __name__ == "__main__":
    main()
