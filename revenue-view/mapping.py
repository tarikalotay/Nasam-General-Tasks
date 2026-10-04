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
AS_OF = '2026-10-04'
BILLED_MONTH = '2026-08'     # newest month with ISSUED invoices — what validate() compares against
DRAFT_MONTH  = '2026-09'     # drafted by the platform 3 Oct, not yet released
SOURCE = 'Nasam platform billing — NASAM-ORG-* invoice line items (Aug issued, Sep drafted), plus the تعديل المنظمة dialog for switched-off channels'

ORGS = {
    'Alfaris Group': dict(on={'Trendyol': 6.0, 'Noon': 6.0, 'Amazon Retail': 6.0}, off=['Salla'],
                          fee=2500.0, src='NASAM-ORG-6-08-2026; Amazon Retail from the Sep draft'),
    'Inivita':       dict(on={'Amazon': 7.0, 'Noon': 7.0, 'Trendyol': 7.0}, off=[], fee=1500.0,
                          src='NASAM-ORG-3-08-2026'),
    'Nokush':        dict(on={'Amazon': 7.0, 'Noon': 7.0, 'Salla': 7.0}, off=[], fee=0.0,
                          src='NASAM-ORG-4-08-2026 — no fee line, by agreement'),
    'Wadi Halfa':    dict(on={'Trendyol': 4.5, 'Amazon Retail': 4.0}, off=[], fee=0.0,
                          src='NASAM-ORG-70-08-2026 — the 2,000 fee was dropped on release; retail from the Sep draft'),
    # Dar Sonbol has never been invoiced a fee or any commission: its only document is INV-000159
    # (4,000 setup, Jun 2026). The organization record carries 8,000/mo, which no invoice has used.
    'Dar Sonbol':    dict(on={}, off=['Salla'], fee=0.0, fee_on_record=8000.0,
                          src='org dialog 13 Sep 2026; the Sep draft NASAM-ORG-86-09-2026 charges the 8,000 for the first time'),
}
# Channels that started selling too recently for the platform to have billed them yet. Each needs a
# decision before its first full month closes, which is what validate() reports.
PENDING = {
    ('Inivita', 'Salla'): 'connected 10 Sep 2026 and sold 215,870 in September, but the September draft '
                          'itemises Amazon, Noon and Trendyol and still carries no Salla line — is it 7% '
                          'like Invita\'s other channels, or no-commission like the other Salla stores?',
}

# Channels Nasam bills BY HAND in Wafeq that the platform's own invoices never produce. This is not
# a commission switch — the money is charged, it just does not come out of the billing engine, so it
# depends on someone remembering to raise it.
PLATFORM_GAP = {
    ('Wadi Halfa', 'Ninja Retail'): 'billed by hand at 4%; the platform has never produced a Ninja '
                                    'Retail line, including on the September draft against 13,232 received',
}

# What the platform DRAFTED for September (created 3 Oct, status DRAFT — not billed until released).
# Recorded here because a draft states the platform's intent for the closing month before the ledger
# does, and two of these change standing answers. Totals are the drafted invoice totals.
DRAFTED = {
    'Alfaris Group': dict(total=6992.82, fee=2500.0, on={'Trendyol': 6.0, 'Noon': 6.0, 'Amazon Retail': 6.0},
                          note='12 Amazon Retail PO lines — every one a PO that closed in JULY, so retail '
                               'commission is running two months behind the deliveries'),
    'Inivita':       dict(total=3012.51, fee=1500.0, on={'Amazon': 7.0, 'Noon': 7.0, 'Trendyol': 7.0},
                          note='still no Salla line, against 215,870 of September Salla sales'),
    'Nokush':        dict(total=120.59, fee=0.0, on={'Amazon': 7.0, 'Salla': 7.0, 'Noon': 7.0},
                          note='unchanged terms'),
    'Wadi Halfa':    dict(total=2038.15, fee=2000.0, on={'Amazon Retail': 4.0},
                          note='the 2,000 monthly fee is back after being dropped from the August invoice; '
                               'two July retail POs billed; no Ninja Retail line at all, against 13,232 received'),
    'Dar Sonbol':    dict(total=8000.0, fee=8000.0, on={},
                          note='the first invoice ever raised for this client beyond the June setup fee, and '
                               'the first to charge the 8,000 — it settles which figure applies, but still '
                               'carries no commission on 694,011 of September Salla sales'),
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
    for (ck, ch), why in sorted(PLATFORM_GAP.items()):
        c = sum(comm_cc.get((ck, ch, m), 0.0) for m in months)
        out.append(('x', ck, ch, why + f' — {c:,.2f} booked in the window by hand'))
    for ck, d in sorted(DRAFTED.items()):
        out.append(('d', ck, '—', f"drafted {d['total']:,.2f} for {DRAFT_MONTH}"
                                  + (f" (fee {d['fee']:,.0f})" if d['fee'] else ' (no fee)')
                                  + ' — ' + d['note']))
    unconf = sorted({k for k, c in known} - confirmed())
    if unconf:
        out.append(('i', ', '.join(unconf), '—', 'no platform invoice to read — still on rate-card terms'))
    return out


def is_pending(client, channel):
    return (client, channel) in PENDING
