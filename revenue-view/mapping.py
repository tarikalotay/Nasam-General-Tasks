# mapping.py — what the Nasam PLATFORM actually charges each client: which channels carry commission,
# at what rate, and the monthly fee. Nasam fixed this mapping in the platform in Sep 2026, so the
# platform — not the rate card — is the authority on whether a channel is invoiced.
#
# SOURCE, and its one limitation. The per-channel toggle itself (العمولة سارية / بلا عمولة in
# تعديل المنظمة) is NOT exposed in the read layer — mcp_read has no organization or channel-mapping
# view. What IS exposed is the toggle's consequence: the platform's own monthly invoice, whose line
# items name each commissioned channel, its rate and the order count, plus the رسوم شهرية fee line.
# Those invoices are read through the billing tool, and they are the same documents Wafeq holds (the
# NASAM-ORG-<org>-<MM>-<YYYY> numbers appear in both), so this is the billing engine's own output
# rather than a second opinion about it.
#
# So: a channel listed in `on` is one the platform demonstrably billed, at the rate it billed. A
# channel in `off` is one that sells but which the platform deliberately does not bill — that is
# read off the organization dialog by eye, or inferred from a channel with real GMV and no line on
# an invoice that itemises every other channel. `off` is therefore the weaker half of this table:
# when the read layer gains an organization view, replace it and drop this note.
# A channel with commission off still syncs its orders and still counts in sales; only its
# commission leaves the invoice. Never drop its GMV.
#
# HOW TO REFRESH (weekly run): read the newest NASAM-ORG-* invoice per client in full (billing tool,
# document='invoices', pass the id) and copy each commission line's channel and rate plus the
# رسوم شهرية amount into ORGS, then move AS_OF. Keys are build.py client keys.
AS_OF = '2026-09-20'
BILLED_MONTH = '2026-08'
SOURCE = 'Nasam platform billing — NASAM-ORG-* invoice line items (Aug 2026), plus the تعديل المنظمة dialog for switched-off channels'

ORGS = {
    'Alfaris Group': dict(on={'Trendyol': 6.0, 'Noon': 6.0}, off=['Salla'], fee=2500.0,
                          src='NASAM-ORG-6-08-2026'),
    'Inivita':       dict(on={'Amazon': 7.0, 'Noon': 7.0, 'Trendyol': 7.0}, off=[], fee=1500.0,
                          src='NASAM-ORG-3-08-2026'),
    'Nokush':        dict(on={'Amazon': 7.0, 'Noon': 7.0, 'Salla': 7.0}, off=[], fee=0.0,
                          src='NASAM-ORG-4-08-2026 — no fee line, by agreement'),
    'Wadi Halfa':    dict(on={'Trendyol': 4.5}, off=[], fee=0.0,
                          src='NASAM-ORG-70-08-2026 — the 2,000 fee was dropped on release'),
    # Dar Sonbol has never been invoiced a fee or any commission: its only document is INV-000159
    # (4,000 setup, Jun 2026). The organization record carries 8,000/mo, which no invoice has used.
    'Dar Sonbol':    dict(on={}, off=['Salla'], fee=0.0, fee_on_record=8000.0,
                          src='org dialog 13 Sep 2026; no platform invoice exists for this client'),
}
# Channels that started selling too recently for the platform to have billed them yet. Each needs a
# decision before its first full month closes, which is what validate() reports.
PENDING = {
    ('Inivita', 'Salla'): 'connected 10 Sep 2026; no commission line yet — is it 7% like Invita\'s '
                          'other channels, or no-commission like the other Salla stores?',
}


def rate(client, channel):
    o = ORGS.get(client)
    return None if not o else o['on'].get(channel)


def commission_on(client, channel):
    """True = billed, False = deliberately not billed, None = the platform has not been read for it."""
    o = ORGS.get(client)
    if not o: return None
    if channel in o['on']: return True
    if channel in o['off']: return False
    return None


def fee(client):
    o = ORGS.get(client)
    return None if not o else o.get('fee')


def confirmed():
    return set(ORGS)


def validate(known, gmv_cc, comm_cc, fee_c, rate_obs, months, closed_month):
    """Hold the platform's mapping against what the workbook bills.

    known        {(client, channel)} the workbook has any figure for
    gmv_cc       (client, channel, month) -> sales
    comm_cc      (client, channel, month) -> commission billed
    fee_c        client -> {month: monthly fee billed}
    rate_obs     (client, channel) -> set of rates seen on the invoices
    Returns [(severity, who, channel, finding)] — 'x' needs a decision, 'i' is informational.
    """
    out = []
    for ck, o in sorted(ORGS.items()):
        for ch, r in sorted(o['on'].items()):
            g = gmv_cc.get((ck, ch, closed_month), 0.0)
            c = comm_cc.get((ck, ch, closed_month), 0.0)
            if abs(c) < 0.005 and g > 0.005:
                out.append(('x', ck, ch, f'platform bills this channel at {r:g}% and it sold {g:,.0f} '
                                         f'in {closed_month}, but no commission is booked that month'))
            seen = {x for x in rate_obs.get((ck, ch), set())}
            if seen and r not in seen:
                out.append(('x', ck, ch, f'platform billed {r:g}%, the ledger shows '
                                         + ' / '.join(f'{x:g}%' for x in sorted(seen))))
        for ch in sorted(o['off']):
            c = sum(comm_cc.get((ck, ch, m), 0.0) for m in months)
            g = gmv_cc.get((ck, ch, closed_month), 0.0)
            if abs(c) > 0.005:
                out.append(('x', ck, ch, f'commission is switched off, yet {c:,.2f} is booked in the window'))
            elif g > 0.005:
                out.append(('i', ck, ch, f'commission off by agreement — {g:,.0f} of sales in {closed_month} '
                                         f'earns nothing and is shown for visibility only'))
        f, got = o.get('fee'), fee_c.get(ck, {}).get(closed_month, 0.0)
        if f and abs(got - f) > 0.005:
            out.append(('x', ck, '—', f'platform fee {f:,.0f}/mo, ledger shows {got:,.2f} in {closed_month}'))
        if not f and abs(got) > 0.005:
            out.append(('x', ck, '—', f'no fee line on the platform invoice, yet {got:,.2f} is booked in {closed_month}'))
        onrec = o.get('fee_on_record')
        if onrec and not f:
            out.append(('x', ck, '—', f'organization record holds {onrec:,.0f}/mo but no invoice has ever charged it'))
        mapped = set(o['on']) | set(o['off'])
        for (kk, ch) in sorted(known):
            if kk == ck and ch not in mapped and ch != 'Amazon Retail' \
               and gmv_cc.get((ck, ch, closed_month), 0.0) > 0.005:
                out.append(('i', ck, ch, 'sells but appears on no platform invoice — not mapped either way'))
    for (ck, ch), why in sorted(PENDING.items()):
        out.append(('x', ck, ch, why))
    unconf = sorted({k for k, c in known} - confirmed())
    if unconf:
        out.append(('i', ', '.join(unconf), '—', 'no platform invoice to read — still on rate-card terms'))
    return out


def is_pending(client, channel):
    return (client, channel) in PENDING
