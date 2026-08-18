# Pull all Wafeq invoices + lookups into sources/wafeq_api_snapshot.json.
# Auth: reads ACCOUNTING_API_KEY (or WAFEQ_API_KEY) from the environment — the key is NEVER stored in this repo.
#   export ACCOUNTING_API_KEY=...   then:  python3 fetch_wafeq.py
import os, sys, json, urllib.request

KEY=os.environ.get("ACCOUNTING_API_KEY") or os.environ.get("WAFEQ_API_KEY")
if not KEY:
    sys.exit("ACCOUNTING_API_KEY not set — add it to the environment (Claude Code environment settings), never to this repo.")
BASE="https://api.wafeq.com/v1"
HERE=os.path.dirname(os.path.abspath(__file__))

def get(path):
    req=urllib.request.Request(BASE+path, headers={"Authorization":f"Api-Key {KEY}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def get_all(resource):
    out=[]; page=1
    while True:
        d=get(f"/{resource}/?page={page}&page_size=100")
        out+=d.get("results",[])
        if not d.get("next"): break
        page+=1
    return out

snap={r: get_all(r) for r in ("invoices","contacts","items","projects")}
dest=os.path.join(HERE,"sources","wafeq_api_snapshot.json")
json.dump(snap, open(dest,"w"), ensure_ascii=False)
print("saved", dest, "|", {k:len(v) for k,v in snap.items()})
