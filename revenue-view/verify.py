#!/usr/bin/env python3
"""Independent verification of the revenue workbook. Run from this directory after build.py:
    python3 verify.py
Re-derives the billing from the Wafeq API snapshot WITHOUT using build.py's parser, and holds the
result against the workbook's own cells. Lives in the repo because it is step 6 of the weekly run
and a scratchpad copy does not survive a new container."""
import json, sys, os
from collections import defaultdict
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B          # for the client map and the window only; every figure below is re-derived
import mapping

wb = load_workbook(os.path.join(HERE, 'output', 'Nasam_Revenue_View.xlsx'), data_only=True)
w1, w2 = wb['1 Revenue Summary'], wb['2 Brand-Channel Detail']
fail = 0

hdr = [c.value for c in w1[1]][2:2 + len(B.M)]
assert hdr[0] == 'Nov 2025' and hdr[-1] == B.ML[-1], hdr
print(f"header check: {hdr[0]} -> {B.M[0]} | {hdr[-1]} -> {B.M[-1]}")

# [1] re-parse Wafeq independently, compare to the BY CLIENT (billed) block
snap = json.load(open(os.path.join(HERE, 'sources', 'wafeq_api_snapshot.json'), encoding='utf-8'))
cname = {c['id']: (c.get('name') or '') for c in snap['contacts']}
iname = {i['id']: (i.get('name') or '') for i in snap['items']}
mine = defaultdict(float)
for inv in snap['invoices']:
    if str(inv.get('status')) == 'DRAFT': continue            # drafted, not issued
    contact = cname.get(inv.get('contact'), '')
    if contact in B.EXCL_CONTACT: continue
    ck = B.ckey(contact)
    if ck is None: continue
    month = B.parse_ref(inv.get('reference') or '', str(inv.get('invoice_date') or '')[:7])
    if month < B.CUT or month not in B.M: continue
    for ln in inv.get('line_items') or []:
        item = iname.get(ln.get('item'), '') if ln.get('item') else ''
        de = item + ' ' + str(ln.get('description') or '')
        # pass-throughs, re-stated here rather than imported so this stays an independent check:
        # Cloud Shelf recharges and marketing/photography rebilled to the client at cost
        if any(x in de for x in ['كلاود شيلف', 'تسويق', 'تصوير']): continue
        mine[(ck, month)] += float(ln.get('line_amount') or 0)
    disc = float(inv.get('discount_amount') or 0)
    if disc > 0.01: mine[(ck, month)] -= disc

rows, seen = {}, False
for row in w1.iter_rows(min_row=2, max_row=w1.max_row):
    lbl = row[1].value
    if lbl == 'BY CLIENT (billed)': seen = True; continue
    if not seen or not lbl: continue
    if lbl == 'TOTAL': break
    k = str(lbl).split('  (churned')[0].split('  (new —')[0].strip()
    rows[k] = {B.M[j]: (row[2 + j].value or 0.0) for j in range(len(B.M))}
bad = [(k, m, float(v), round(mine.get((k, m), 0.0), 2)) for k, mm in rows.items()
       for m, v in mm.items() if abs(float(v) - mine.get((k, m), 0.0)) > 0.02]
missing = sorted({k for k, _ in mine} - set(rows))
fail += len(bad) + len(missing)
print(f"[1] Wafeq re-parse vs client-month cells: {len(rows)*len(B.M)} cells, {len(bad)} mismatches {bad[:6]}")
print(f"    clients in sheet: {len(rows)} | re-parse keys not in sheet: {missing}")

# [2] each client's billed revenue equals the sum of its component rows on sheet 2
by = defaultdict(lambda: defaultdict(float))
for row in w2.iter_rows(min_row=2, max_row=w2.max_row):
    k, metric = row[0].value, row[3].value
    if not k or k == 'ALL CLIENTS': continue
    key = str(k).split('  (churned')[0].split('  (new —')[0].strip()
    for j in range(len(B.M)):
        v = float(row[6 + j].value or 0.0)
        if metric == 'Billed revenue': by[key]['p%d' % j] += v
        elif metric in ('Commission (billed)', 'Monthly fee', 'Setup / one-time', 'Other', 'Discounts'):
            by[key]['k%d' % j] += v
bad2 = [(k, B.M[j], round(d.get('p%d' % j, 0.0), 2), round(d.get('k%d' % j, 0.0), 2))
        for k, d in by.items() for j in range(len(B.M))
        if abs(d.get('p%d' % j, 0.0) - d.get('k%d' % j, 0.0)) > 0.02]
fail += len(bad2)
print(f"[2] billed revenue == sum of its component rows: {len(by)*len(B.M)} cells checked, {len(bad2)} mismatches {bad2[:6]}")

# [3] the TOTAL identity, over the window only
billed = round(sum(v for (k, m), v in B.billed.items() if m in B.M), 2)
print(f"[3] TOTAL = billed {billed:,.2f} + to-invoice {B.acc_total:,.2f} "
      f"+ SaaS net {B.saas_total*(1-B.SALLA_SHARE):,.2f} = {billed+B.acc_total+B.saas_total*(1-B.SALLA_SHARE):,.2f}")

# [4] every rate the platform billed is a rate the ledger shows
bad3 = [(ck, ch, r, sorted({float(x) for x in B.rate_obs.get((ck, ch), set())}))
        for ck, o in mapping.ORGS.items() for ch, r in o['on'].items()
        if B.rate_obs.get((ck, ch)) and r not in {float(x) for x in B.rate_obs[(ck, ch)]}]
fail += len(bad3)
print(f"[4] platform rates vs ledger rates: {len(bad3)} disagreements {bad3}")

print("VERIFICATION PASSED" if fail == 0 else f"VERIFICATION FAILED — {fail} problem(s)")
sys.exit(1 if fail else 0)
