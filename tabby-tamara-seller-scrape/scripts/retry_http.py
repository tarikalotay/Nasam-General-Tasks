#!/usr/bin/env python3
"""Second pass: retry failed https crawls over plain http."""
import json, threading, queue
import crawl_contacts as cc

RETRY_STATUSES = {"URLError", "TimeoutError", "RemoteDisconnected",
                  "ConnectionResetError", "IncompleteRead", "http_503", "http_502"}

def main():
    latest = {}
    for line in open("contacts.jsonl", encoding="utf-8"):
        try:
            c = json.loads(line)
            latest[c["dkey"]] = c
        except Exception:
            pass
    jobs = [{"dkey": k, "website": "http://" + v["website"][len("https://"):]}
            for k, v in latest.items()
            if v["status"] in RETRY_STATUSES and v["website"].startswith("https://")]
    print(f"retrying over http: {len(jobs)}", flush=True)
    qq = queue.Queue()
    for j in jobs:
        qq.put(j)
    lock = threading.Lock()
    out = open("contacts.jsonl", "a", encoding="utf-8")
    n = [0]
    def worker():
        while True:
            try:
                j = qq.get_nowait()
            except queue.Empty:
                return
            res = cc.process(j)
            if res["status"] == "ok":
                with lock:
                    out.write(json.dumps(res, ensure_ascii=False) + "\n")
            with lock:
                n[0] += 1
                if n[0] % 250 == 0:
                    out.flush(); print(f"retry progress: {n[0]}/{len(jobs)}", flush=True)
    threads = [threading.Thread(target=worker, daemon=True) for _ in range(80)]
    for t in threads: t.start()
    for t in threads: t.join()
    out.close()
    print("retry pass complete", flush=True)

if __name__ == "__main__":
    main()
