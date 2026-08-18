#!/usr/bin/env python3
"""Crawl ONE domain and print a JSON line. Single-threaded by design:
Python threads + subprocess fork deadlocked at scale, so concurrency is
provided externally by xargs -P (independent processes)."""
import json, sys
import crawl_contacts as cc

def main():
    line = sys.argv[1]
    dkey, _, website = line.partition("\t")
    try:
        res = cc.process({"dkey": dkey, "website": website})
    except Exception as e:
        res = {"dkey": dkey, "website": website, "status": type(e).__name__,
               "final_url": "", "emails": [], "phones": [], "whatsapp": [],
               "instagram": [], "twitter": [], "tiktok": [], "snapchat": [], "linkedin": []}
    sys.stdout.write(json.dumps(res, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
