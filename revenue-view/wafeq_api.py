# Load the Wafeq API snapshot (sources/wafeq_api_snapshot.json) into per-line rows for build.py.
# Produced by fetch_wafeq.py. Replaces the manual xlsx export as the billing source.
import json, os
HERE=os.path.dirname(os.path.abspath(__file__))
SNAP=os.path.join(HERE,'sources','wafeq_api_snapshot.json')

def available():
    return os.path.exists(SNAP)

def load():
    snap=json.load(open(SNAP,encoding='utf-8'))
    cname={c['id']:(c.get('name') or '') for c in snap['contacts']}
    iname={i['id']:(i.get('name') or '') for i in snap['items']}
    rows=[]
    for inv in snap['invoices']:
        first=True
        for li in inv.get('line_items',[]):
            rows.append(dict(
                num=inv['invoice_number'], date=(inv.get('invoice_date') or '')[:10],
                contact=cname.get(inv.get('contact'),''),
                amount=float(inv.get('amount') or 0), balance=float(inv.get('balance') or 0),
                status=inv.get('status') or '', disc=float(inv.get('discount_amount') or 0),
                ref=inv.get('reference') or '',
                item=iname.get(li.get('item'),'') if li.get('item') else '',
                desc=li.get('description') or '', lam=float(li.get('line_amount') or 0),
                first=first))
            first=False
    return rows
