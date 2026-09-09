#!/usr/bin/env python3
"""Write resolved websites into the ClickUp "URL" field of Brands Leads tasks.

Reads a JSON map {task_id: {name, website, source, confidence}} and fills the
URL custom field, skipping any task that already has one (nothing is overwritten).

    export CLICKUP_API=pk_...
    python3 scripts/fill_lead_websites.py sites.json --dry-run
    python3 scripts/fill_lead_websites.py sites.json
"""
import argparse, json, os, sys, time, urllib.error, urllib.request

URL_FIELD = "fccd0a4c-7d41-4377-997c-5a9df50030cf"      # "URL" on the Brands Leads list
API = "https://api.clickup.com/api/v2"


def call(url, token, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Authorization": token,
                                          "Content-Type": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.loads(r.read().decode() or "{}")
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < 3:
                time.sleep(2 ** attempt * 2)
                continue
            raise
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sites", help="JSON map of task_id -> {website, ...}")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    token = os.environ.get("CLICKUP_API")
    if not token:
        sys.exit("CLICKUP_API is not set.")

    sites = json.load(open(args.sites))
    todo = {tid: v for tid, v in sites.items() if v.get("website")}
    print(f"{len(todo)} leads with a website to write "
          f"({'dry run' if args.dry_run else 'live'})")

    written = skipped = failed = 0
    for i, (tid, v) in enumerate(todo.items(), 1):
        task = call(f"{API}/task/{tid}", token)
        current = next((f.get("value") for f in task.get("custom_fields", [])
                        if f["id"] == URL_FIELD), None)
        if current:
            skipped += 1
            print(f"  skip  {v['name'][:28]:<28} already has {current[:40]}")
            continue
        if args.dry_run:
            written += 1
        else:
            try:
                call(f"{API}/task/{tid}/field/{URL_FIELD}", token, "POST",
                     {"value": v["website"]})
                written += 1
            except Exception as e:
                failed += 1
                print(f"  FAIL  {v['name'][:28]:<28} {e}")
        if i % 25 == 0:
            print(f"  … {i}/{len(todo)}", flush=True)
        time.sleep(0.7)                                  # stay under 100 req/min

    print(f"written: {written}  skipped (already set): {skipped}  failed: {failed}")


if __name__ == "__main__":
    main()
